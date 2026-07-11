import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


import unittest
from unittest.mock import patch, MagicMock
from ffmpeg import FFmpeg, Map, FileInputOptions, InputFile, apply, apply2
from ffmpeg.filters import HorizontalStack, Scale, BaseFilter, VerticalStack, AudioMix


class TestFFmpeg(unittest.TestCase):
    """Tests FFmpeg filter handling and apply/apply2 behavior.

    This test suite verifies that:
    - filter flags are serialized correctly into ffmpeg filter syntax,
    - filters are registered exactly once in the filter graph,
    - apply() rejects filters with multiple outputs,
    - apply2() rejects filters with a single output.
    """

    def setUp(self):
        self.video = InputFile(
            "video.mp4", FileInputOptions(duration=5, frame_rate=30)
        ).get_stream(0, stream_name="v")

        self.audio = InputFile("audio.mp3", FileInputOptions(duration=5))

        self.filter_script_name = "filters_tests.txt"

    def doCleanups(self) -> None:
        # Clean up any temporary files if created
        if os.path.exists(self.filter_script_name):
            os.remove(self.filter_script_name)
        return super().doCleanups()

    def test_filter_handling(self):
        class DummyFilter(BaseFilter):
            pass

        filter = DummyFilter("dummyfilter")
        filter.flags = {"x": 1, "y": "2", "z": True, "a": None}
        filtered = apply(filter, self.video)
        ff = FFmpeg().output(Map(filtered), path="broken.mp4")
        cmd = ff.compile()

        filter = cmd[cmd.index("-filter_complex") + 1]

        self.assertIn("dummyfilter", filter)
        self.assertIn("x=1", filter)  # int no change
        self.assertIn("y=2", filter)  # str no change
        self.assertIn("z=1", filter)  # bool will be int
        self.assertNotIn("a=", filter)  # None will be skiped

    def test_filter_register_once(self):
        scale = Scale(width=1280, height=720)
        filtered = apply(scale, self.video)
        ff = FFmpeg().output(Map(filtered), path="scaled.mp4")
        command = ff.compile()

        # The scale filter should only be registered once
        filter = command[command.index("-filter_complex") + 1]
        self.assertEqual(filter.count("scale"), 1)

        with self.assertRaises(RuntimeError):
            apply(scale, self.video)

    def test_wrong_apply(self):
        # if user use apply with multiple outputs filter should raise error
        filter = BaseFilter("dummy")
        filter.output_count = 2
        with self.assertRaises(ValueError):
            apply(filter, self.video)

        # if user use apply2 with single output filter should raise error
        filter = BaseFilter("dummy")
        filter.output_count = 1
        with self.assertRaises(ValueError):
            apply2(filter, self.video)

    def test_stack_apply_equivalence(self):
        inputs = [
            InputFile("1.mp4"),
            InputFile("2.mp4"),
            InputFile("3.mp4"),
            InputFile("4.mp4"),
        ]

        filter_classes = [HorizontalStack, VerticalStack, AudioMix]

        for stack_cls in filter_classes:
            c1 = apply(stack_cls(*inputs))
            c2 = apply(stack_cls(), *inputs)
            c3 = apply(stack_cls(*inputs[:2]), *inputs[2:])

            cmd1 = FFmpeg().output(Map(c1), path="1.mp4").compile()
            cmd2 = FFmpeg().output(Map(c2), path="2.mp4").compile()
            cmd3 = FFmpeg().output(Map(c3), path="3.mp4").compile()

        self.assertCountEqual(cmd1[:-1], cmd2[:-1], cmd3[:-1])

        filter_idx = cmd1.index("-filter_complex") + 1

        self.assertEqual(cmd1[filter_idx], cmd2[filter_idx])
        self.assertEqual(cmd2[filter_idx], cmd3[filter_idx])
        self.assertEqual(cmd1[filter_idx], cmd3[filter_idx])
