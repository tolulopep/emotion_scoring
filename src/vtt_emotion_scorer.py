import os
import webvtt
import logging
import scipy.ndimage.filters
import matplotlib.pyplot as plt
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
    logger = logging.getLogger('VTTEmotionScorer')
    output_folder = os.getcwd() + "/output/"

    def __init__(self, file_path):
        '''
        Extracts captions in vtt file available in file_path and calculate emotion scores using classifier model. Creates output folder if it does not exist

        Parameters:
          file_path (string): Path to vtt file
        '''
        if not os.path.exists(VTTEmotionScorer.output_folder):
            try:
                os.makedirs(VTTEmotionScorer.output_folder)
            except Exception as e:
                VTTEmotionScorer.logger.exception(
                    'Unable to create output folder')
                raise e

        try:
            captions = webvtt.read(file_path)
        except Exception as e:
            VTTEmotionScorer.logger.exception('Unable to parse VTT file')
            raise e

        self._scores = dict()
        self._end_times = []
        self._title = os.path.basename(file_path).title()

        for each_caption in captions:
            self._end_times.append(each_caption.end)
            prediction = VTTEmotionScorer.classifier(
                each_caption.text.replace("\n", " ").strip())
            for row in prediction[0]:
                self._scores[row['label']] = [
                    *self._scores.get(row['label'], []), row['score']]

        for key in self._scores:
            try:
                assert len(self._scores[key]) == len(self._end_times)
            except Exception as e:
                VTTEmotionScorer.logger.exception(
                    'Fatal error when calculating emotions for ' + key)
                raise e

    def save_to_file(self, output_file):
        '''
        Saves the plot of emotions to the provided output file 

        Parameters:
          output_file (string): Output file to save to inside the output folder
        '''
        for key in self._scores:
            ysmoothed = scipy.ndimage.filters.gaussian_filter1d(
                self._scores[key], sigma=5)
            plt.plot(self._end_times, ysmoothed, label=key)
        plt.xlabel('Timestamp')
        plt.ylabel('Score')
        plt.title(self._title)
        plt.xticks(rotation=75)
        plt.legend()
        plt.grid()
        plt.gcf().set_size_inches(50, 10)
        try:
            plt.savefig(VTTEmotionScorer.output_folder + output_file)
        except Exception as e:
            VTTEmotionScorer.logger.exception(
                'Unable to save to output file')
            raise e
