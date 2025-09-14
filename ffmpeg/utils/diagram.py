"""
This module provides functionality to visualize the FFmpeg filter graph using Graphviz.
It constructs a directed graph representing inputs, filters, and outputs, and saves it as an image file.
It is not part of the core ffmpeg functionality and is intended for debugging and visualization purposes.

Requires:
    graphviz module (install via pip and binaries as needed).
"""

import itertools

from ..ffmpeg import FFmpeg
from ..inputs import BaseInput
from ..inputs.streams import StreamSpecifier


def format_flags(flag: dict):
    return ", ".join([f"{k}={v}" for k, v in flag.items()])


def draw_filter_graph(
    ffmpeg: FFmpeg,
    file_name: str = "filter_graph",
    format: str = "png",
    fontsize: int = 10,
    dpi: int = 140,
) -> None:
    """
    Visualises the FFmpeg filter graph and saves it as an image.

    Note:
        Requires: graphviz module

    Args:
        output_path:   File path *without* extension where the diagram is written.
        format:        Output format accepted by Graphviz (png, svg, …).
    """
    try:
        from graphviz import Digraph
    except ImportError as e:
        e.add_note(
            "Please Install `graphviz` \nSee Docs Installation at: https://graphviz.readthedocs.io/en/stable/manual.html#installation"
        )
        raise e

    if not ffmpeg._outputs:
        raise RuntimeError("No outputs defined - add at least one `output()` first.")

    # ── 1. Build the internal graph exactly the same way we do for `compile()` ──
    ffmpeg.reset()
    for out in ffmpeg._outputs:
        for m in out.maps:
            ffmpeg._build_filter(m.node)  # populates _inputs/_filter_nodes

    # ── 2. Start the dot graph ──
    dot = Digraph(name="FFmpegFilterGraph", format=format)
    dot.attr(rankdir="LR", dpi=str(dpi), fontsize=str(fontsize))

    # Helper to assign deterministic unique IDs
    uid = itertools.count()
    node_ids: dict[object, str] = {}

    def add_node(obj, label, shape="box", color="lightgray"):
        if obj not in node_ids:
            node_ids[obj] = f"n{next(uid)}"
            dot.node(node_ids[obj], label, shape=shape, style="filled", fillcolor=color)
        return node_ids[obj]

    # ── 3. Inputs ──
    for idx, inp in enumerate((ffmpeg._inputs)):
        add_node(
            inp,
            f"Input[{idx}]\n{getattr(inp, 'filepath', '')}",
            shape="box",
            color="lightblue",
        )

    # ── 4. Filters and intermediate StreamSpecifiers ──
    stream_nodes: dict[StreamSpecifier, str] = {}
    for f_idx, filt in enumerate(ffmpeg._filter_nodes):
        f_id = add_node(
            filt,
            getattr(filt, "name", filt.__class__.__name__)
            + "\n"
            + format_flags(filt.flags),
            shape="ellipse",
            color="khaki",
        )

        for parent in filt.parent_nodes:
            #  ⤷ 4.a  Parent is a *StreamSpecifier* -----------------------------
            if isinstance(parent, StreamSpecifier):
                # Create StreamSpecifier node (diamond)
                s_id = stream_nodes.get(parent)
                if s_id is None:
                    spec_lbl = "stream" + parent.build_stream_str()
                    s_id = add_node(
                        parent, f"[{spec_lbl}]", shape="diamond", color="gray90"
                    )
                    stream_nodes[parent] = s_id

                    # Edge FROM producer (its .parent) TO the new spec‑node
                    producer = parent.parent
                    prod_id = add_node(
                        producer,
                        getattr(producer, "name", producer.__class__.__name__),
                        shape=("box" if isinstance(producer, BaseInput) else "ellipse"),
                        color=(
                            "lightblue" if isinstance(producer, BaseInput) else "khaki"
                        ),
                    )
                    dot.edge(prod_id, s_id)

                # Edge FROM spec‑node TO the current filter
                dot.edge(s_id, f_id)

            #  ⤷ 4.b  Parent is a regular BaseInput / BaseFilter ---------------
            else:
                p_id = add_node(
                    parent,
                    getattr(parent, "name", parent.__class__.__name__),
                    shape=("box" if isinstance(parent, BaseInput) else "ellipse"),
                    color=("lightblue" if isinstance(parent, BaseInput) else "khaki"),
                )
                dot.edge(p_id, f_id)

    # ── 5. Outputs ──
    for out_idx, out in enumerate(ffmpeg._outputs):
        out_id = add_node(out, out.path, shape="box", color="palegreen")
        for m in out.maps:
            n = m.node

            # Create intermediate StreamSpecifier node if needed
            if isinstance(n, StreamSpecifier):
                if n not in stream_nodes:
                    spec_lbl = "stream" + n.build_stream_str()
                    # spec_lbl = "S"
                    s_id = add_node(n, f"[{spec_lbl}]", shape="diamond", color="gray90")
                    stream_nodes[n] = s_id

                    # Edge from parent (BaseInput/BaseFilter) ➝ StreamSpecifier
                    parent = n.parent
                    p_id = add_node(
                        parent,
                        getattr(parent, "name", parent.__class__.__name__),
                        shape=("box" if isinstance(parent, BaseInput) else "ellipse"),
                        color=(
                            "lightblue" if isinstance(parent, BaseInput) else "khaki"
                        ),
                    )
                    dot.edge(p_id, s_id)
                else:
                    s_id = stream_nodes[n]

                dot.edge(s_id, out_id)

            else:
                # Direct BaseInput/Filter passed without stream spec
                src_id = add_node(
                    n,
                    getattr(n, "name", n.__class__.__name__),
                    shape=("box" if isinstance(n, BaseInput) else "ellipse"),
                    color=("lightblue" if isinstance(n, BaseInput) else "khaki"),
                )
                dot.edge(src_id, out_id)
    # ── 6. Render ──

    dot.render(filename=file_name, cleanup=True)
