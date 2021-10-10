#!/usr/bin/env python
import os
import sys
import argparse
import scipy.ndimage.filters
import matplotlib.pyplot as plt
from src.vtt_emotion_scorer import VTTEmotionScorer


def save_to_file(title, scores, end_times, output_file):
    '''
    Saves the plot of emotions to the provided output file 

    Parameters:
       title (string): The title to display as legend on the image
       scores (dict): A dictionary containing key value map of labels and their associated list of scores for each caption in the vtt file
       end_times (list): A list containing all the start times for each caption in the vtt file
       output_file (string): The destination file name
    '''
    for key in scores:
        ysmoothed = scipy.ndimage.filters.gaussian_filter1d(
            scores[key], sigma=5)
        plt.plot(end_times, ysmoothed, label=key)
    plt.xlabel('Timestamp')
    plt.ylabel('Score')
    plt.title(title)
    plt.xticks(rotation=75)
    plt.legend()
    plt.grid()
    plt.gcf().set_size_inches(85, 30)
    try:
        plt.savefig(output_file)
    except Exception:
        sys.exit('Unable to save to output file')


def main(input_file, output_folder, output_file):
    '''
    Entry point to the application 
    '''
    if input_file == None:
        sys.exit('No input file was provided')
    if input_file.endswith(".vtt") == False:
        sys.exit('Only VTT files are accepted')
    if os.path.isfile(input_file) == False:
        sys.exit('Input file does not exist')
    if output_file == None:
        sys.exit('No output file name was provided')
    if output_file.endswith(".png") == False:
        sys.exit('Output file must be a png')
    if not os.path.exists(output_folder):
        try:
            os.makedirs(output_folder)
        except Exception:
            sys.exit(
                'Unable to create output folder')
    try:
        scores, end_times = VTTEmotionScorer(
            input_file).extract_emotion_scores_and_end_times()
        save_to_file(
            os.path.basename(output_file).title(), scores, end_times, output_folder + "/" + output_file)
        sys.exit('Emotions successfully scored.')
    except Exception:
        sys.exit('Unable to score emotions.')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-f", "--file", required=True,
                    help="single vtt file location")
    ap.add_argument("-o", "--output_file", required=True,
                    help="file name to save image to")
    args = vars(ap.parse_args())
    main(args["file"], os.getcwd() + "/output/", args["output_file"])
