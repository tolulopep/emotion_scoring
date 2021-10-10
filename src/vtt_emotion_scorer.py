import webvtt
import logging
from transformers import pipeline
from dataclasses import dataclass

classifier = pipeline("text-classification",
                      model='bhadresh-savani/distilbert-base-uncased-emotion', return_all_scores=True)


class VTTEmotionScorer:
    '''
    Emotion scorer implementation for .vtt files

    Attributes
    ----------
    classfier: Text classification model for generating scorers for each caption in the vtt file
    logger: Logger variable
    _captions: The captions in the vtt file dict
    '''

    logger = logging.getLogger('VTTEmotionScorer')

    def __init__(self, file_path):
        '''
        Extracts captions in vtt file available in file_path and calculate emotion scores using classifier model. Creates output folder if it does not exist

        Parameters:
          file_path (string): Path to vtt file
        '''
        try:
            self._captions = webvtt.read(file_path)
        except Exception as e:
            VTTEmotionScorer.logger.exception('Unable to parse VTT file')
            raise e

    def extract_emotion_scores_and_end_times(self):
        '''
        Extracts emotion scores and end times from the captions in the vtt file

        Returns:
          dict: A dictionary containing key value map of labels and their associated list of scores for each caption in the vtt file
          list: A list containing all the start times for each caption in the vtt file

        Raises:
          Exception: Exception is thrown when the length of the scores for a label is different from the length of start time list.
        '''
        scores = dict()
        end_times = []
        for each_caption in self._captions:
            end_times.append(each_caption.end)
            prediction = classifier(
                each_caption.text.replace("\n", " ").strip())
            for row in prediction[0]:
                scores[row['label']] = [
                    *scores.get(row['label'], []), row['score']]

        return scores, end_times
