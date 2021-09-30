#!/usr/bin/env python

import shlex
import subprocess
import sys
import json
import os
import argparse
import wave
import webvtt
from transformers import pipeline
from timeit import default_timer as timer

classifier = pipeline("text-classification",
                          model='bhadresh-savani/distilbert-base-uncased-emotion', return_all_scores=True)

# Custom functions
def extract_scores_and_start_times(file_path):
    scores = dict()
    start_times = []
    for each_caption in webvtt.read(file_path)[2::4]:
      start_times.append(each_caption.start)
      prediction = classifier(each_caption.text)
      for row in prediction[0]:
        scores[row['label']] = [
                    *scores.get(row['label'], []), row['score']]
    return scores, start_times
    
def main():

    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-f", "--file", required=False, help="single vtt file location")
    args = vars(ap.parse_args())
    
    if args["file"] == '':
      raise RuntimeError('No file was provided')
    if os.path.splitext(args["file"])[1] != "vtt":
      raise RuntimeError('Only VTT files are accepted')

    try:
        emotion_scorer = create_emotion_scorer(filename)
    except Exception as error:
       # current_app.logger.error("Error calculating emotion scores", error)
       # return "Invalid file", 400
    

    
    args["file"]

    



    # sphinx-doc: python_ref_model_stop
    model_load_end = timer() - model_load_start
    print('Loaded model and in {:.3}s.'.format(model_load_end), file=sys.stderr)

    desired_sample_rate = ds.sampleRate()

    # print('Loading scorer from files {}'.format(SCORER_FILE), file=sys.stderr)
    # scorer_load_start = timer()
    # ds.enableExternalScorer(SCORER_FILE)
    # scorer_load_end = timer() - scorer_load_start
    # print('Loaded scorer in {:.3}s.'.format(scorer_load_end), file=sys.stderr)

    # TODO: lm_alpha and lm_beta are omitted because they are being used from scorer

    if args["audio"] is not None:
        transcribe_(args["audio"], desired_sample_rate, ds)


    # read video_urls or video_locs file and transcribe one by one
    elif args["list"] is not None:
        with open(args["list"], "r") as f:
            locations = f.read()

        locations = locations.split("\n")

        for audio_loc in locations:
            transcribe_(audio_loc, desired_sample_rate, ds)

    else:
        raise ValueError("[ERROR] Check your command line arguments, there is something wrong!")

if __name__ == '__main__':
    main()