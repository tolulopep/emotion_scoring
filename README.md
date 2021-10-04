# Emotion Scoring

Emotion Scoring is a Python project for extracting emotion information from text. 

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install dependencies in the project.

```bash
pip3 install -r requirements.txt
```

## Run application

```bash
python .\run.py -f sample.vtt -o output.png
```

-f is the path to the vtt file and -o is the target file output that will be saved in the output folder (automatically created)

## Run tests

```bash
python -m unittest test.test_vtt_emotion_scorer
```

## Demo
![demo](screen-capture.gif)
