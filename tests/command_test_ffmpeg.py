import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


import unittest
from unittest.mock import patch, MagicMock
from ffmpeg import FFmpeg, Map, FileInputOptions, InputFile, apply, apply2
from ffmpeg.filters import Scale, BaseFilter


class TestFFmpeg(unittest.TestCase):

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

    def test_output_compilation(self):
        ff = FFmpeg().output(Map(self.video), Map(self.audio), path="output.mp4")
        command = ff.compile(overwrite=True)

        self.assertIn("ffmpeg", command[0])
        self.assertIn("-y", command)  # overwrite flag
        self.assertEqual("output.mp4", command[-1])
        self.assertEqual(command.count("-map"), 2)

    def test_generate_inlink_name_for_input(self):
        ff = FFmpeg()
        ff._is_input_exporting(self.video)
        name = ff._generate_inlink_name(self.video)
        self.assertEqual(name, "0:v:0")  # 0th input, video stream, 0th index

    @patch("ffmpeg.ffmpeg.subprocess.Popen")
    def test_run_with_mocked_process(self, mock_popen):
        mock_proc = MagicMock()
        mock_proc.stdout.readline.side_effect = [
            "frame=1\n",
            "progress=end\n",
            "",  # simulate progress output
        ]
        mock_proc.wait.return_value = 0
        mock_proc.returncode = 0
        mock_popen.return_value = mock_proc

        ff = FFmpeg().output(Map(self.video), path="output.mp4")
        ff.run(progress_callback=lambda data: self.assertIn("progress", data))

        self.assertTrue(mock_popen.called)
        self.assertEqual(mock_proc.wait.call_count, 1)

    def test_export_helper(self):
        from ffmpeg import export, __version__

        print(__version__)
        ff = export(self.video, path="exported.mp4")
        command = ff.compile()
        self.assertIn("ffmpeg", command[0])
        self.assertIn("-y", command)  # overwrite flag

        self.assertEqual("exported.mp4", command[-1])
        self.assertEqual(command.count("-map"), 1)

    def test_compile_without_overwrite(self):
        ff = FFmpeg().output(Map(self.video), path="no_overwrite.mp4")
        command = ff.compile(overwrite=False)

        self.assertNotIn("-y", command)
        self.assertIn("-n", command)
        self.assertEqual("no_overwrite.mp4", command[-1])

    def test_multiple_outputs(self):
        ff = (
            FFmpeg()
            .output(Map(self.video), path="output1.mp4")
            .output(Map(self.video), path="output2.mkv")
        )
        command = ff.compile()

        self.assertIn("output1.mp4", command)
        self.assertIn("output2.mkv", command)

    def test_input_export_once(self):
        ff = FFmpeg()
        ff._is_input_exporting(self.video)
        # Re-exporting the same input should not add it again
        ff._is_input_exporting(self.video)
        self.assertEqual(len(ff._inputs), 1)

    def test_filter_handling(self):
        class DummyFilter(BaseFilter):
            pass

        filter = DummyFilter("dummyfilter")
        filter.flags = {"x": 1, "y": "2", "z": True, "a": None}
        filtered = apply(filter, self.video)
        ff = FFmpeg().output(Map(filtered), path="broken.mp4")
        command = ff.compile()
        cmd = command

        filter = cmd[cmd.index("-filter_complex") + 1]

        self.assertIn("dummyfilter", filter)
        self.assertIn("x=1", filter)  # int no change
        self.assertIn("y=2", filter)  # str no change
        self.assertIn("z=1", filter)  # bool will be int
        self.assertNotIn("a=", filter)  # None will be skiped

    def test_filter_chain_application(self):
        filtered = apply(Scale(width=1280, height=720), self.video)
        ff = FFmpeg().output(Map(filtered), path="scaled.mp4")
        command = ff.compile()

        self.assertIn("-filter_complex", command)  # Check if video filter is applied
        self.assertIn("scale=width=1280:height=720", " ".join(command))
        self.assertEqual("scaled.mp4", command[-1])

    def test_filter_script(self):
        filtered = apply(Scale(width=1280, height=720), self.video)
        ff = FFmpeg(
            use_filter_file=True, filter_script_file=self.filter_script_name
        ).output(Map(filtered), path="scaled.mp4")
        command = ff.compile()

        self.assertIn("-filter_complex_script", command)

        # Check if the filter script file is created and contains the correct filter
        script_index = command.index("-filter_complex_script") + 1
        script_path = command[script_index]
        self.assertTrue(os.path.exists(script_path))
        with open(script_path, "r") as f:
            content = f.read()

        self.assertIn("scale=width=1280:height=720", content)

    def test_filter_long_script(self):

        input_clip = self.video
        times = 20
        for _ in range(
            times
        ):  # Chain multiple scales to ensure it exceeds typical command line length
            input_clip = apply(Scale(width=1280, height=720), input_clip)

        ff = FFmpeg(
            use_filter_file=True, filter_script_file=self.filter_script_name
        ).output(Map(input_clip), path="long_scaled.mp4")
        command = ff.compile()
        self.assertIn("-filter_complex_script", command)

        # make sure the scale filter is in the script
        script_index = command.index("-filter_complex_script") + 1
        script_path = command[script_index]

        self.assertTrue(os.path.exists(script_path))
        with open(script_path, "r") as f:
            content = f.read()

        self.assertIn("scale=width=1280:height=720", content)

        # count how many scale filters are in the script
        self.assertEqual(content.count("scale=width=1280:height=720"), times)

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

    def test_global_flags_default_reset(self):
        ff = FFmpeg()

        default_flags = ff._global_flags
        ff.reset()
        self.assertEqual(default_flags, ff._global_flags)

    def test_global_flags_custom(self):
        ff = FFmpeg()
        ff.reset()
        flags = ["someflag", "some_more_flag"]

        ff.output(Map(InputFile("input.mp4")), path="out.mp4")

        ff.add_global_flag(*flags)
        commamd = ff.compile()

        self.assertIn(flags[0], commamd)
        self.assertIn(flags[1], commamd)

    def test_compile_consistency(self):
        filtered = apply(Scale(width=1280, height=720), self.video)
        ff = FFmpeg().output(Map(filtered), path="scaled.mp4")

        self.assertEqual(ff.compile(), ff.compile())
        self.assertEqual(ff.compile(), ff.compile())

    def test_outputs(self):
        ff = (
            FFmpeg()
            .output(Map(self.video), path="out1.mp4")
            .output(Map(self.audio), path="out2.mp3")
        )

        self.assertEqual(len(ff._outputs), 2)
        self.assertEqual(ff._outputs[0].path, "out1.mp4")
        self.assertEqual(ff._outputs[1].path, "out2.mp3")


if __name__ == "__main__":
    unittest.main()
