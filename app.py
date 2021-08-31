import imghdr
import os
import webvtt
from flask import Flask, render_template, request, redirect, url_for, abort, \
    send_from_directory, jsonify
from werkzeug.utils import secure_filename
from transformers import pipeline

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.vtt']
app.config['UPLOAD_PATH'] = './templates'
classifier = pipeline("text-classification",
                      model='bhadresh-savani/distilbert-base-uncased-emotion', return_all_scores=True)


@app.errorhandler(413)
def too_large(e):
    return "File is too large", 413


@app.route('/')
def index():
    files = os.listdir(app.config['UPLOAD_PATH'])
    return render_template('index.html', files=files)


@app.route('/', methods=['POST'])
def upload_files():
    uploaded_file = request.files['file']
    filename = os.path.join(
        app.config['UPLOAD_PATH'], secure_filename(uploaded_file.filename))
    json = {}
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS']:
            return "Invalid image", 400
        uploaded_file.save(filename)
        json = extract_data(filename)
        os.remove(filename)
    return jsonify(indent=2, sort_keys=False, result=json)


@app.route('/uploads/<filename>')
def upload(filename):
    return send_from_directory(app.config['UPLOAD_PATH'], filename)


def extract_data(dst):
    sub = webvtt.read(dst)[2::4]
    scores = dict()
    start_times = []
    for caption in sub:
        start_times.append(caption.start)
        prediction = classifier(caption.text)
        for row in prediction[0]:
            scores[row['label']] = [
                *scores.get(row['label'], []), row['score']]
    return {"scores": scores, "start_times": start_times}
