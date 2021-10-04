import os
import tempfile
import unittest
import logging
from pathlib import Path
from webvtt.errors import MalformedFileError
from src.vtt_emotion_scorer import VTTEmotionScorer


class TestVTTEmotionScorer(unittest.TestCase):
    target_file = "test.png"
    input_file = "sample.vtt"

    def __init__(self, x):
        unittest.TestCase.__init__(self, x)
        VTTEmotionScorer.logger.setLevel(logging.CRITICAL)
        VTTEmotionScorer.output_folder = tempfile.mkdtemp()

    def test_when_invalid_file_is_provided(self):
        with self.assertRaises(MalformedFileError):
            VTTEmotionScorer("README.md").save_to_file(
                TestVTTEmotionScorer.target_file)

    def test_successful_execution(self):
        VTTEmotionScorer(TestVTTEmotionScorer.input_file).save_to_file(
            TestVTTEmotionScorer.target_file)
        path = Path(VTTEmotionScorer.output_folder +
                    TestVTTEmotionScorer.target_file)
        assert path.is_file()


if __name__ == '__main__':
    unittest.main()
