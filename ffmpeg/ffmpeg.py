"""
This module provides methods to build and run FFmpeg with fine control commands.

Example:
    ```python
    from ffmpeg import FFmpeg, InputFile, Map

    ffmpeg = FFmpeg()

    ffmpeg.output(Map(clip), path="output.mp4").run()

    # or for async
    await ffmpeg.output(Map(clip), path="output.mp4").run_async()

    or multiple outputs
    ffmpeg.output(Map(clip1), path="output1.mp4").output(Map(clip2), path="output2.mp4").run()
    ```

For simple usecase use `export` function it allows to export in one line, see example below
    ```python
    from ffmpeg import export, InputFile

    clip = InputFile("input.mp4")
    export(clip, path="output.mkv").run()
    ```
"""

import asyncio
import logging
import subprocess
from pathlib import Path
from typing import Any, Callable, Coroutine, Literal, Optional, Self

from .exception.exceptions import FFmpegCompileError, FFmpegException
from .filters import BaseFilter
from .inputs import BaseInput
from .inputs.streams import StreamSpecifier
from .output.output import Map, OutFile
from .utils.commons import parse_value, wrap_sqrtbrkt

logger = logging.getLogger("ffmpeg")


class FFmpeg:
    def __init__(
        self,
        path: str = "ffmpeg",
        use_filter_file: bool = False,
        filter_script_file: str = "filters.txt",
    ) -> None:
        """
        This class provides methods to construct and execute FFmpeg commands.
        either Run or Compile the command to get the command list and run it manually.

        Initialize the FFmpeg command builder.

        Args:
            path: Path to the ffmpeg executable.".
            use_filter_file: Whether to use a filter script file,useful for very long filter graphs.
            filter_script_file: Path to the filter script file if use_filter_file is True.
        """

        self.ffmpeg_path = path
        self._inputs: list[BaseInput] = []
        self._filter_nodes: list[BaseFilter] = []
        self._outputs: list[OutFile] = []
        self._node_count: int = 0
        self._global_flags: dict[str, str | float | None] = {"-hide_banner": None}

        self.filter_script_file = filter_script_file
        self.use_filter_file = use_filter_file

        # Set Defaults
        self.reset(reset_global=True)

    def set_ffmpeg_path(self, path: str):
        """
        Set the path to the ffmpeg executable.
        """

        self.ffmpeg_path = path

    def reset(self, reset_global: bool = True) -> Self:
        """Reset all compilation data added"""
        self._inputs = []
        self._filter_nodes = []
        self._node_count = 0
        if reset_global:
            self._global_flags = {"-hide_banner": None}
        return self

    def add_global_flag(self, key: str, value: str | float | None = None) -> Self:
        """Adds additional FFmpeg flags, avoiding duplicates"""
        self._global_flags[key] = value
        return self

    def _build_global_flags(self) -> list[str]:
        cmd = []
        for key, value in self._global_flags.items():
            cmd.append(key)
            if value is not None:
                cmd.append(str(value))
        return cmd

    def _is_input_exporting(self, node: BaseInput | StreamSpecifier) -> bool:
        """Check if Output is Input without any filter applied"""
        if isinstance(node, StreamSpecifier):
            node = node.parent

        if isinstance(node, BaseInput):
            if node not in self._inputs:
                self._inputs.append(node)
            return True
        return False

    def _get_outname(self, i: Any, j: Any, stream_char: str = "") -> str:
        """
        make names for link names

        Note:
            stream_char should not be use in outlink name generation
        """
        return f"n{i}o{j}{stream_char}"

    def _generate_inlink_name(
        self, parent: BaseInput | StreamSpecifier | BaseFilter
    ) -> str:
        """Get different types of links that ffmpeg uses with different types of Object"""
        stream_specifier = ""

        if isinstance(parent, StreamSpecifier):
            stream_specifier = parent.build_stream_str()
            output_n = parent.output_number
            parent = parent.parent

        if isinstance(parent, BaseInput):
            input_name = f"{self._inputs.index(parent)}{stream_specifier}"  # idx
        else:
            input_name = self._get_outname(
                self._filter_nodes.index(parent), output_n, stream_specifier
            )
        return input_name

    def _build_filter(
        self, last_node: BaseInput | StreamSpecifier
    ) -> list[Any] | Literal[""]:
        """Builds the final FFmpeg chains"""

        # If the output is Base Input return no need to add a filter
        if self._is_input_exporting(last_node):
            return ""

        self._inputs_tmp: list[BaseInput] = []
        flat_graph: list[BaseFilter] | None = self._flatten_graph(last_node)

        if flat_graph is None:
            return ""

        self._filter_nodes.extend(flat_graph[::-1])
        self._inputs.extend(self._inputs_tmp[::-1])
        del self._inputs_tmp

        filter_chain = []

        for filter in flat_graph[::-1]:

            filter_block = ""

            # gather parents
            for parent in filter.parent_nodes:
                filter_block += wrap_sqrtbrkt(self._generate_inlink_name(parent))

            # gather args
            filter_block += filter._build()

            # gather outlink
            for j in range(filter.output_count):
                filter_block += wrap_sqrtbrkt(self._get_outname(self._node_count, j))

            self._node_count += 1
            filter_chain.append(filter_block)

        return filter_chain

    def _flatten_graph(
        self, node: BaseInput | StreamSpecifier
    ) -> list[BaseFilter] | None:
        stack = [node]
        visited_filters = set()
        collected_nodes = []
        while stack:
            current = stack.pop()
            if isinstance(current, StreamSpecifier):
                current = current.parent
            if isinstance(current, BaseInput):
                if current not in self._inputs_tmp:
                    self._inputs_tmp.append(current)
                continue
            if isinstance(current, BaseFilter):
                if current in self._filter_nodes or current in visited_filters:
                    continue
                visited_filters.add(current)
                collected_nodes.append(current)
                stack.extend(reversed(current.parent_nodes))
        return collected_nodes or None

    def _build_inputs(self) -> list[str]:

        sub_command = []
        for inp in self._inputs:
            sub_command.extend(inp._build_input_flags())
        return sub_command

    def _build_map(self, map: Map, map_index) -> list[str]:

        node = map.node
        stream = self._generate_inlink_name(node)

        if isinstance(node, StreamSpecifier):
            node = node.parent

        if not isinstance(node, BaseInput):
            stream = wrap_sqrtbrkt(stream)

        flags = map._build(stream, map_index=map_index)
        return flags

    def compile(self, overwrite: bool = True) -> list[str]:
        """
        Generate the full FFmpeg command as a list of arguments.

        This method collects and combines all the necessary parts of the FFmpeg command,
        including global flags, input definitions, filter graphs, mapping, output flags,
        and output file paths. It ensures that the command is constructed in the correct
        order and with all required options for execution.

        Returns:
            The complete FFmpeg command as a list of arguments.
        """

        if len(self._outputs) < 1:
            raise FFmpegCompileError("No outputs defined for the FFmpeg command.")

        self.reset(reset_global=False)

        if overwrite:
            self.add_global_flag("-y")
        else:
            self.add_global_flag("-n")

        self.add_global_flag("-loglevel", "error")

        command = [self.ffmpeg_path, *self._build_global_flags()]
        # First flatten filters to add inputs automatically from last node order matters here
        filters = []
        for output in self._outputs:
            for map_ in output.maps:
                filters.extend(self._build_filter(map_.node))

        if inputs := self._build_inputs():
            command.extend(inputs)

        if filters:
            if self.use_filter_file:
                Path(self.filter_script_file).write_text(";\n".join(filters))
                command.extend(("-filter_complex_script", self.filter_script_file))
            else:
                command.extend(("-filter_complex", ";".join(filters)))

        for output in self._outputs:
            for i, maps in enumerate(output.maps):  # one output can have multiple maps
                command.extend(self._build_map(maps, i))

            command.extend(output._build())

        return list(map(str, command))

    def output(
        self,
        *maps: Map | BaseInput | StreamSpecifier,
        path: str,
        metadata: Optional[dict[str, str]] = None,
        **kwargs,
    ) -> Self:
        """
        Create output for the with streams mapped to it.

        Args:
            *maps: One or more `Map` objects or input nodes to include in the output.
            path: The file path for the output media file.
            metadata: Metadata to be added to the output file.
            **kwargs (dict[str, Any]): Additional keyword arguments representing output-specific
        """
        wrapped_maps = [
            Map(node) if not isinstance(node, Map) else node for node in maps
        ]
        self._outputs.append(OutFile(wrapped_maps, path, metadata=metadata, **kwargs))
        return self

    def run(
        self,
        progress_callback: Optional[Callable[[dict], None]] = None,
        progress_period: float = 0.5,
        overwrite: bool = True,
    ) -> None:
        """
        Run the FFmpeg command.

        Args:
            progress_callback:\
            Function that can be used to track progress of the process running data can be mix of None and actual values
            progress_period: Set period at which progress_callback is called
            overwrite: overwrite the output if already exists
        """

        stdout = None
        stderr = subprocess.PIPE

        # If progress_callback: function is provided capture the outputs
        if progress_callback:
            stdout = subprocess.PIPE
            self.add_global_flag("-progress", "pipe:1")
            self.add_global_flag("-nostats")
            self.add_global_flag("-stats_period", progress_period)

        command = self.compile(overwrite=overwrite)
        logger.debug(f"Running: {command}")  # Debugging output

        # Start FFmpeg process
        process = subprocess.Popen(
            command,
            stdout=stdout,
            stderr=stderr,
            universal_newlines=True,
            bufsize=1,
        )

        if progress_callback is not None:
            assert process.stdout is not None

            # Read progress data
            progress_data = {}

            for line in iter(process.stdout.readline, ""):
                line = line.strip()
                if "=" in line:
                    key, value = line.split("=", 1)
                    progress_data[key] = parse_value(value.strip())

                if "progress" in progress_data:
                    try:
                        progress_callback(progress_data)
                    except Exception as e:
                        logger.exception(
                            f"Error in progress_callback: {e}. Continuing..."
                        )
                    progress_data.clear()  # Reset for next update

            process.stdout.close()
        process.wait()  # Ensure process completes

        if process.returncode != 0:
            raise FFmpegException(process.stderr.read(), process.returncode)

    async def run_async(
        self,
        progress_callback: Optional[Callable[[dict], Coroutine[Any, Any, None]]] = None,
        progress_period: float = 0.5,
        overwrite: bool = True,
    ) -> None:
        """
        Asynchronously run the FFmpeg command.

        Args:
            progress_callback:
                Function that can be used to track progress of the process running data can be mix of None and actual values
            progress_period: Set period at which progress_callback is called
            overwrite: overwrite the output if already exists

        """

        stdout = None
        stderr = asyncio.subprocess.PIPE

        if progress_callback:
            stdout = asyncio.subprocess.PIPE
            self.add_global_flag("-progress", "pipe:1")
            self.add_global_flag("-nostats")
            self.add_global_flag("-stats_period", progress_period)

        command = self.compile(overwrite=overwrite)
        logger.debug(f"Running (async): {command}")

        process = await asyncio.create_subprocess_exec(
            *command,
            stdout=stdout,
            stderr=stderr,
        )

        if progress_callback:
            assert process.stdout is not None

            progress_data = {}

            while True:
                line = await process.stdout.readline()
                if not line:
                    break
                line = line.decode().strip()
                if "=" in line:
                    key, value = line.split("=", 1)
                    progress_data[key] = parse_value(value.strip())

                if "progress" in progress_data:
                    if progress_callback:
                        try:
                            await progress_callback(progress_data)
                        except Exception as e:
                            logger.exception(
                                f"Error in progress_callback: {e}. Continuing..."
                            )
                    progress_data.clear()

        await process.wait()

        if process.returncode != 0:
            stderr_output = ""
            if process.stderr:
                stderr_output = await process.stderr.read()
            raise FFmpegException(stderr_output, process.returncode)


def export(*nodes: BaseInput | StreamSpecifier, path: str, **kwargs) -> FFmpeg:
    """
    Exports a clip by processing the given input nodes and saving the output to the specified path.

    Args:
        nodes: One or more input nodes representing media sources.
        path : The output file path where the exported clip will be saved.
        kwargs (dict[str, Any]): flags for Output
        
    Returns:
        FFmpeg instance configured with the given inputs and output path.
    """
    return FFmpeg().output(*(Map(node) for node in nodes), path=path, **kwargs)
