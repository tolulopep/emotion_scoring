import os
import webvtt
from transformers import pipeline


class VTTEmotionScorer:
    '''
    Emotion scorer implementation for .vtt files

    Attributes
    ----------
    classifier: Pipeline
        Text classification model for generating scorers for each caption in the vtt file
    _scores : dict
        A dictionary containing key value map of labels and their associated list of scores for each caption in the vtt file
    _start_times : list
        A list containing all the start times for each caption in the vtt file
    '''
    classifier = pipeline("text-classification",
                          model='bhadresh-savani/distilbert-base-uncased-emotion', return_all_scores=True)

    def __init__(self, file_path):
        '''
        Extracts captions in vtt file available in file_path and calculate emotion scores using classifier model.

        Parameters:
          file_path (string): Path to vtt file
        '''
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
        '''
        Getter method for the _scores dictionary set in constructor
        Returns:
          dict: key value map of labels and their associated list of scores
        '''
        return self._scores

    @property
    def start_times(self):
        '''
        Getter method for the _start_times list set in constructor
        Returns:
          list: list containing all the start times
        '''
        return self._start_times
