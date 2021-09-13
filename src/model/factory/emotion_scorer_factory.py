import os
from src.model.service.vtt_emotion_scorer import VTTEmotionScorer


def create_emotion_scorer(file_path):
    '''
    Retrieves right object for scoring based on the file extension
    Parameters:
      file_path (string): Path to file
    Returns:
                  object: Appropriate emotion scorer for processing the file
    Raises:
      ValueError: When there is no appropriate emotion scorer object for file
    '''
    extension = os.path.splitext(file_path)[1]
    if extension.endswith(".vtt"):
        return VTTEmotionScorer(file_path)
    else:
        raise ValueError('Unable to retrieve the right emotion scorer')
