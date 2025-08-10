"""
This module provides methods to build and run FFmpeg with fine control commands.

For simple usecase use `export`

"""

import logging
import subprocess
from pathlib import Path
from typing import Any, Callable, Literal, Optional, Self

from .exception.exceptions import FFmpegException
from .filters import BaseFilter
from .inputs import BaseInput
from .inputs.streams import StreamSpecifier
from .output.output import Map, OutFile
from .utils.commons import build_flags, parse_value, wrap_sqrtbrkt

logger = logging.getLogger("ffmpeg")


class FFmpeg:
    """FFmpeg Command Builder"""

    def __init__(self) -> None:

        self.ffmpeg_path = "ffmpeg"
        self._inputs: list[BaseInput] = []
        self._filter_nodes: list[BaseFilter] = []
        self._outputs: list[OutFile] = []
        self.node_count: int = 0
        self._global_flags: dict[str, str | float | None] = {}

        self.filter_file = "filters.txt"
        self.use_filter_file = False

        # Set Defaults
        self.reset(reset_global=True)

    def set_ffmpeg_path(self, path: str):
        self.ffmpeg_path = path

    def reset(self, reset_global=True) -> Self:
        """Reset all compilation data added"""
        self._inputs = []
        self._filter_nodes = []
        self.node_count = 0
        if reset_global:
            self._global_flags = {"-hide_banner": None}
        return self

    def add_global_flag(self, key: str, value: str | float | None = None) -> Self:
        """Adds additional FFmpeg flags, avoiding duplicates"""
        self._global_flags[key] = value
        return self

    def buid_global_flags(self):
        cmd = []
        for key, value in self._global_flags.items():
            cmd.append(key)
            if value is not None:
                cmd.append(str(value))
        return cmd

    def is_input_exporting(self, node: BaseInput | StreamSpecifier) -> bool:
        """Check if Output is Input without any filter applied"""
        if isinstance(node, StreamSpecifier):
            node = node.parent

        if isinstance(node, BaseInput):
            if node not in self._inputs:
                self._inputs.append(node)
            return True
        return False

    def generate_link_name(self, i, j, stream_char="") -> str:
        """
        make names for link names

        Note:
            stream_char should not be use in outlink name generation
        """
        return f"n{i}o{j}{stream_char}"

    def generate_inlink_name(self, parent: BaseInput | StreamSpecifier) -> str:
        """Get different types of links that ffmpeg uses with different types of Object"""
        stream_specifier = ""

        if isinstance(parent, StreamSpecifier):
            stream_specifier = parent.build_stream_str()
            output_n = parent.output_number
            parent = parent.parent

        if isinstance(parent, BaseInput):
            input_name = f"{self._inputs.index(parent)}{stream_specifier}"  # idx
        else:
            input_name = self.generate_link_name(
                self._filter_nodes.index(parent), output_n, stream_specifier
            )
        return input_name

    def build_filter(
        self, last_node: BaseInput | StreamSpecifier
    ) -> list[Any] | Literal[""]:
        """Builds the final FFmpeg chains"""

        # If the output is Base Input return no need to add a filter
        if self.is_input_exporting(last_node):
            return ""

        self._inputs_tmp: list[BaseInput] = []
        flat_graph: list[BaseFilter] | None = self.flatten_graph(last_node)

        if flat_graph is None:
            return ""

        self._filter_nodes.extend(flat_graph[::-1])
        self._inputs.extend(self._inputs_tmp[::-1])

        filter_chain = []

        for filter in flat_graph[::-1]:

            filter_block = ""

            # gather parents
            for parent in filter.parent_nodes:
                filter_block += wrap_sqrtbrkt(self.generate_inlink_name(parent))

            # gather args
            filter_block += filter.build()

            # gather outlink
            for j in range(filter.output_count):
                filter_block += wrap_sqrtbrkt(
                    self.generate_link_name(self.node_count, j)
                )

            self.node_count += 1
            filter_chain.append(filter_block)

        return filter_chain

    def flatten_graph(
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

    def build_inputs(self) -> list[str]:

        sub_command = []
        for inp in self._inputs:
            sub_command.extend(inp.build_input_flags())
        return sub_command

    def build_map(
        self, map: Map, map_index
    ) -> tuple[Literal["-map"], str, *tuple[Any, ...]]:

        node = map.node
        stream = self.generate_inlink_name(node)

        if isinstance(node, StreamSpecifier):
            node = node.parent

        if not isinstance(node, BaseInput):
            stream = wrap_sqrtbrkt(stream)

        flags = map.build(map_index=map_index)
        return ("-map", stream, *flags)

    def compile(self, overwrite=True) -> list[str]:
        """
        Generate the command
        This fuction gather and combine all of the different part of the command.

        """

        if len(self._outputs) < 1:
            raise RuntimeError()

        self.reset(reset_global=False)

        if overwrite:
            self.add_global_flag("-y")
        else:
            self.add_global_flag("-n")

        self.add_global_flag("-loglevel", "error")

        command = [self.ffmpeg_path, *self.buid_global_flags()]
        # First flatten filters to add inputs automatically from last node order matters here
        filters = []
        for output in self._outputs:
            for map_ in output.maps:
                filters.extend(self.build_filter(map_.node))

        if inputs := self.build_inputs():
            command.extend(inputs)

        if filters:
            if self.use_filter_file:
                Path(self.filter_file).write_text(";\n".join(filters))
                command.extend(("-filter_complex_script", self.filter_file))
            else:
                command.extend(("-filter_complex", ";".join(filters)))

        for output in self._outputs:
            for i, maps in enumerate(output.maps):  # one output can have multiple maps
                command.extend(self.build_map(maps, i))

            command.extend(build_flags(output.kvflags))
            command.append(output.path)

        return list(map(str, command))

    def output(self, *maps: Map, path: str, **kvflags) -> Self:
        """
        Create output for the command with map and output specific flags and the path for the output.

        Args:
            maps: add output for export
            path: output file path
            kvflags: flags for output

        """
        self._outputs.append(OutFile(maps, path, **kvflags))
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
            progress_callback:
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

        if progress_callback:
            assert process.stdout is not None

            # Read progress data
            progress_data = {}

            for line in iter(process.stdout.readline, ""):
                line = line.strip()
                if "=" in line:
                    key, value = line.split("=", 1)
                    progress_data[key] = parse_value(value.strip())

                if "progress" in progress_data:
                    if progress_callback:
                        progress_callback(progress_data)
                    progress_data.clear()  # Reset for next update

            process.stdout.close()
        process.wait()  # Ensure process completes

        if process.returncode != 0:
            raise FFmpegException(process.stderr.read(), process.returncode)


def export(*nodes: BaseInput | StreamSpecifier, path: str, **kwargs) -> FFmpeg:
    """
    Exports a clip by processing the given input nodes and saving the output to the specified path.

    Args:
        nodes (BaseInput | StreamSpecifier): One or more input nodes representing media sources.
        path (str): The output file path where the exported clip will be saved.
        kwargs (dict[str, Any]): flags for Output
    Returns:
        FFmpeg: An FFmpeg instance configured with the given inputs and output path.
    """
    return FFmpeg().output(*(Map(node) for node in nodes), path=path, **kwargs)
