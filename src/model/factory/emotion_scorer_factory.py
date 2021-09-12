import os
from src.model.service.vtt_emotion_scorer import VTTEmotionScorer

class EmotionScorerFactory(object):

  @staticmethod
  def create_emotion_scorer(file_path):
    extension = os.path.splitext(file_path)[1]
    if extension.endswith(".vtt"):
      return VTTEmotionScorer(file_path)
    else:
      raise ValueError('Unable to retrieve the right emotion scorer')

