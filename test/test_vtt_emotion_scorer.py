import unittest
import logging
from pathlib import Path
from webvtt.errors import MalformedFileError
from src.vtt_emotion_scorer import VTTEmotionScorer


class TestVTTEmotionScorer(unittest.TestCase):
    input_file = "sample.vtt"

    def __init__(self, x):
        unittest.TestCase.__init__(self, x)
        VTTEmotionScorer.logger.setLevel(logging.CRITICAL)

    def test_when_invalid_file_is_provided(self):
        with self.assertRaises(MalformedFileError):
            VTTEmotionScorer("README.md")

    def test_successful_execution(self):
        scores, end_times = VTTEmotionScorer(TestVTTEmotionScorer.input_file).extract_emotion_scores_and_end_times()
        for key in scores:
                assert len(scores[key]) == len(end_times)
        
if __name__ == '__main__':
    unittest.main()
