#!/usr/bin/env python
import os
import sys
import argparse
from src.vtt_emotion_scorer import VTTEmotionScorer


def main():
    '''
    Entry point to the application 
    '''
    ap = argparse.ArgumentParser()
    ap.add_argument("-f", "--file", required=False,
                    help="single vtt file location")
    ap.add_argument("-o", "--output", required=False,
                    help="file name to save image to")
    args = vars(ap.parse_args())
    if args["file"] == None:
        sys.exit('No input file was provided')
    if args["file"].endswith(".vtt") == False:
        sys.exit('Only VTT files are accepted')
    if os.path.isfile(args["file"]) == False:
        sys.exit('Input file does not exist')
    if args["output"] == None:
        sys.exit('No output file name was provided')
    if args["output"].endswith(".png") == False:
        sys.exit('Output file must be a png')
    try:
        VTTEmotionScorer(args["file"]).save_to_file(args["output"])
        sys.exit('Emotions successfully scored.')
    except Exception:
        sys.exit('Unable to score emotions.')


if __name__ == '__main__':
    main()
