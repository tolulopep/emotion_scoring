import os
import webvtt
from transformers import pipeline


class VTTEmotionScorer:
    classifier = pipeline("text-classification",
                          model='bhadresh-savani/distilbert-base-uncased-emotion', return_all_scores=True)

    def __init__(self, file_path):
        self._scores = dict()
        self._start_times = []
        _captions = webvtt.read(file_path)[2::4]
        for each_caption in _captions:
            self._start_times.append(each_caption.start)
            prediction = VTTEmotionScorer.classifier(each_caption.text)
            for row in prediction[0]:
                self._scores[row['label']] = [
                    *self._scores.get(row['label'], []), row['score']]

    @property
    def scores(self):
        return self._scores

    @property
    def start_times(self):
        return self._start_times
