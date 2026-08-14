# Architecture

This page explains how `ffmpeg-studio` represents an FFmpeg pipeline internally, how data flows from the objects you build in Python to the actual `ffmpeg` process, and how the library's pieces interface with each other. It's aimed at contributors and advanced users who want to extend the library (new filters, new input types) or just understand what `.run()` is doing under the hood.

## Mental model

FFmpeg itself takes a flat CLI invocation (`-i`, `-filter_complex`, `-map`, output flags), but pipelines are naturally a **graph**: inputs feed filters, filters feed other filters, and everything eventually gets mapped to one or more outputs.

`ffmpeg-studio` lets you build that graph as plain Python objects, then compiles it into the flat CLI form FFmpeg expects only at the last moment. There is no persistent `Graph` class — the graph is implicit in back-references between nodes, and it is walked and flattened lazily by `FFmpeg.compile()`.

Three kinds of node make up the graph:

| Node type | Class | Represents |
| --------- | ----- | ---------- |
| Source | `BaseInput` (`VideoFile`, `ImageFile`, `AudioFile`, `InputFile`, `VirtualVideo`) | A `-i` input, or a synthetic source (e.g. `lavfi`) |
| Transform | `BaseFilter` (`Scale`, `Overlay`, `Concat`, `Split`, …) | One `-filter_complex` node |
| Handle | `StreamSpecifier` | A typed pointer to one output of a source or filter (e.g. "the audio stream of this input", "the second output of this split") |
| Sink | `Map` / `OutFile` | Where a node in the graph exits: `Map` binds one node (input or `StreamSpecifier`) to a `-map`, with its own per-stream flags (codec, metadata); `OutFile` groups one or more `Map`s under a single output path and output-level flags (`crf`, container options, …) |

You never build the CLI string yourself — you wire nodes together with plain function calls, and `FFmpeg` does the topological flattening and argument rendering when you call `.compile()` or `.run()`.

## Building the graph

```python
from ffmpeg import InputFile, apply, FFmpeg
from ffmpeg.filters import Scale, Overlay

bg = InputFile("bg.mp4")
logo = apply(Scale(100, 100), InputFile("logo.png"))
composited = apply(Overlay(x=10, y=10), bg, logo)

FFmpeg().output(composited, path="out.mp4").run()
```

- **Inputs** (`BaseInput` subclasses) wrap a source file/path and its input-side flags (`-ss`, `-t`, etc). `_get_outputs()` gives you a `StreamSpecifier` pointing at that input.
- **Filters** are plain `BaseFilter` instances holding their own flags (e.g. `Scale(100, 100)`). They aren't wired to anything until you connect them.
- **`apply(filter_obj, *parents) -> StreamSpecifier`** registers `parents` as the filter's inputs and returns a handle to its single output. **`apply2(...) -> list[StreamSpecifier]`** does the same for filters with multiple outputs (`Split`, `Concat`).
- Each `BaseFilter` instance can only be wired once — calling `apply`/`apply2` twice on the same filter object raises, preventing accidental graph reuse.
- Because `apply()` returns a `StreamSpecifier`, chaining filters is just passing that return value as the parent of the next `apply()` call — the graph is built functionally, not by mutating a shared object.

`Map` and `OutFile` (in `ffmpeg.output`) sit at the edge of the graph: a `Map` wraps a node (input or `StreamSpecifier`) plus per-stream output flags (codec, metadata); an `OutFile` wraps one or more `Map`s plus a destination path and output-level flags (`crf`, container options, …). `FFmpeg.output(*maps, path=..., **kwargs)` is the entry point that creates these and attaches them to the builder.

Some filters (`scale` is the extreme case) expose dozens of optional FFmpeg parameters. Rather than one constructor with dozens of keyword arguments, filters like `Scale` accept the common ones in `__init__` and expose the rest as chainable `set_*`/`reset_*` methods that mutate `self.flags` and `return self`:

```python
from ffmpeg.filters import Scale

scale = (
    Scale(1280, 720)
    .set_eval(EvalMode.INIT)
    .set_interlacing(InterlacingMode.ON)
    .set_force_divisible_by(2)
)
```

This keeps the common case (`Scale(w, h)`) simple while still allowing every rarely-used FFmpeg option to be set without an unwieldy constructor signature, and reads close to the filter's own documentation (one call per option).

FFmpeg's `enable` option — an expression like `between(t\,2\,5)` that turns a filter on/off based on the current timestamp — is generic: it applies uniformly to any filter that supports timeline editing (`Text`/`drawtext`, `Overlay`, and others), not to one specific filter's domain logic. So instead of living on `BaseFilter` itself (which would imply every filter supports `enable`, and it doesn't), `enable_between`/`enable_after`/`enable_before` are implemented once as `TimelineEditingMixin` (`ffmpeg/filters/mixins/enable.py`) and mixed into whichever filters support it (e.g. `class Text(BaseFilter, TimelineEditingMixin)`). The mixin only assumes `self.flags: dict` exists, so it composes with any filter without needing to know that filter's other options.

## Compiling: graph → CLI arguments

`FFmpeg` (`ffmpeg/ffmpeg.py`) accumulates build state as you call `.output()`:

```
_inputs: list[BaseInput]
_filter_nodes: list[BaseFilter]
_outputs: list[OutFile]
```

Calling `.compile()` does the actual translation:

1. **Flatten each output's graph.** For every `Map` in every `OutFile`, `_flatten_graph()` walks backward from the mapped node through `parent_nodes` (a DFS over filters, resolving `StreamSpecifier.parent` as it goes), collecting the `BaseFilter` ancestors in dependency order and auto-registering any `BaseInput`s it discovers along the way.
2. **Render filter nodes.** Each filter renders itself as `name=k=v:k=v`, and its parents/outputs are rendered as bracketed link names (`[n{filter_index}o{output_index}]`). These are joined with `;` into a single `-filter_complex` string by default. Very large graphs can exceed OS/shell command-length limits as one argument — passing `use_filter_file=True` (and optionally `filter_script_file=...`) to `FFmpeg(...)` writes the same string to a file instead and swaps `-filter_complex "..."` for `-filter_complex_script <path>` in the compiled command; nothing else about graph-building changes, it's purely a transport decision made at compile time.
3. **Render inputs.** Each `BaseInput` contributes its own `-i` flags in registration order — this is what fixes each input's numeric index for `-map`.
4. **Render `-map` / output flags.** Each `Map` resolves its node to either a raw input index (`0:v`) or a filter-graph link name, plus any per-stream flags (`-c:v`, metadata). Each `OutFile` appends its own kv-flags, metadata, and destination path.

The result is a plain list of CLI arguments — `FFmpeg.compile()` returns exactly what you'd type at a terminal. `-filter_complex` is only emitted if the pipeline actually contains filters; a filter-free input→output copy compiles to a minimal `-i ... -map ... out.mp4`.

Calling `.compile()` twice, or inspecting `draw_filter_graph()` (see below), doesn't mutate your original filter objects in a way that breaks a later `.run()` — but note that `_inputs`/`_filter_nodes` are populated as a side effect of flattening, so `compile()` is not purely read-only against the `FFmpeg` instance itself (this is also why `draw_filter_graph` re-runs `_build_filter` to regenerate the same state for visualization).

FFmpeg is strict about wiring: every filter output it creates must be consumed by something, and every filter input must come from a real, previously-defined link — an unreferenced pad or a dangling link name is a hard error, not a warning. Building the `-filter_complex` string by hand is exactly where this bites people (typo a link name, forget to map an output, leave a filter half-wired). Flattening from the mapped outputs backward avoids this class of error by construction: because `_flatten_graph()` starts from what's actually **mapped** and walks backward through `parent_nodes`, only filters that are genuine ancestors of a mapped output ever get emitted. A `BaseFilter` you construct but never `apply()` into a mapped chain simply never appears in the compiled command, and link names (`n{idx}o{idx}`) are assigned during the same walk that emits the filter rather than typed by hand — so the filter definitions and the links between them can't drift out of sync the way handwritten `-filter_complex` strings do.

Rendering itself is also deliberately decentralized: every node — `BaseInput`, `BaseFilter`, `Map`, `OutFile` — owns its own `_build_*` method that turns its state into CLI arguments, rather than `FFmpeg` centrally knowing how to render every possible filter or input. `FFmpeg.compile()` only orchestrates *when* each node renders and how the pieces link together; it stays ignorant of what's inside any given filter's syntax. This matters because FFmpeg's filters don't share one uniform grammar — most are simple `key=value:key=value` pairs, but some have their own quoting/escaping rules (`drawtext`'s `text=`/`fontfile=`, see below), positional-only syntax, or nested expression languages. Keeping rendering on each node means a filter with unusual syntax can special-case itself without `FFmpeg` needing a growing pile of `if filter_name == ...` branches — adding a new filter is adding a new self-contained class, not patching the compiler.

Two helpers, `build_flags` (global/output-level flags) and `build_name_kvargs_format` (filter option strings), apply the same small set of conversions when turning a Python dict into CLI text, so individual filters/inputs don't need to repeat this logic:

- **`bool` → `0`/`1`.** FFmpeg has no native boolean flag value — `True`/`False` are converted to `1`/`0` (e.g. `reset_sar(True)` → `sar=1`), matching what FFmpeg actually expects.
- **`None` → flag is skipped/bare.** In `build_flags`, a `None` value emits the flag name with no value (`{"y": None}` → `["-y"]`), used for boolean-style CLI switches. In filter kwargs (`build_name_kvargs_format`), a `None` value drops the key entirely — this is what lets filter classes default optional parameters to `None` and have them silently omitted from the rendered string instead of requiring every filter to manually build a "only include if set" dict.
- **Text escaping.** Filters that take free-form text (notably `Text`/`drawtext`) run user-supplied strings through `escape_arguments`/`escape_stray_percent` before building the filter string, escaping characters FFmpeg's filter grammar treats as special (`:`, `\`, stray `%`). Without this, a caption containing a colon or backslash would silently corrupt the filter graph syntax (or open a path for filter-string injection from untrusted text) instead of being rendered as literal text.

## Running: process execution and progress

`.run()` / `.run_async()` call `.compile()`, then hand the argument list to `subprocess.Popen` / `asyncio.create_subprocess_exec`.

- Without a `progress_callback`, this is a normal blocking (or awaitable) subprocess call; a non-zero exit code raises `FFmpegException(stderr, return_code)`.
- With a `progress_callback`, the builder additionally passes `-progress pipe:1 -nostats -stats_period N`, telling FFmpeg to emit machine-readable `key=value` progress lines on stdout instead of its normal human-readable stats. stdout is read line by line; each line is parsed (`parse_value` — typed as int/float/`None` for `N/A`/string) and accumulated into a dict. The dict is flushed to your callback every time a `progress` key is seen (FFmpeg emits that key once per stats interval), giving you a live snapshot (`frame`, `fps`, `out_time`, `speed`, …) as encoding proceeds.

This is the same interface for the sync and async run paths — the only difference is whether the underlying subprocess and stdout read loop use `subprocess`/blocking reads or `asyncio`.

## Supporting interfaces

- **`ffprobe`** (`ffmpeg.ffprobe`) shells out to `ffprobe -show_streams -show_format -print_format json` and parses the result. `VideoFile` uses this internally to back `.get_size()`, `.get_duration()`, stream iteration/indexing (`__iter__`, `__getitem__`), and `.audio`/`.video`/`.subtitle` stream lookup — so inspecting a `VideoFile`'s streams transparently probes the real file. Failures raise `FFprobeException`.
- **`ffplay`** (`ffmpeg.ffplay`) is a thin, fire-and-forget wrapper: it builds a flag string from keyword arguments and runs `ffplay` via `subprocess.run(shell=True)` for local playback/preview. It does not participate in the graph model.
- **Expressions** (`ffmpeg.expressions`) provides helpers for building FFmpeg's numeric/eval expression syntax (used in filters that take expressions rather than fixed values, e.g. dynamic overlay positions).
- **`draw_filter_graph`** (`ffmpeg.utils.diagram`) renders the graph FFmpeg will build — inputs, filters, stream specifiers, outputs, with directed edges — as a Graphviz diagram. It's the fastest way to sanity-check a complex pipeline before running it.

## Error handling

Errors are a flat hierarchy, all raised as Python exceptions rather than error codes:

- `FFmpegCompileError` — raised by `.compile()` itself, e.g. when no outputs were defined.
- `FFmpegException(message, return_code)` — raised by `.run()`/`.run_async()` when the `ffmpeg` process exits non-zero; carries the process's stderr and exit code.
- `FFprobeException(FFmpegException)` — same shape, raised by `ffprobe()` failures.

## Extending the library

The two most common extension points both slot into the same graph model:

- **New filter**: subclass `BaseFilter`, set `filter_name` and populate `self.flags` in `__init__`; `output_count` controls whether it should be wired with `apply()` (single output) or `apply2()` (multiple outputs, e.g. a custom split-like filter). No changes to `FFmpeg` are needed — `_flatten_graph` walks any `BaseFilter` uniformly.
- **New input type**: subclass `BaseInput`, implement `_build_input_flags()` to return the `-i`-side CLI arguments for that source. `VideoFile` is the richest example (subclip trimming, ffprobe-backed stream introspection) if you need a template.

## See also

- [API Reference](api_reference/index.md) for the full class/method listing (autogenerated from docstrings).
- [Tutorials](tutorial/making_input.md) for task-oriented, example-first walkthroughs.
- [Mosaic example](example/mosaic.md) for a realistic multi-filter graph built with `apply()`.
