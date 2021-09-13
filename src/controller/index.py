import os
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, jsonify, after_this_request, Blueprint, current_app
from src.model.factory.emotion_scorer_factory import EmotionScorerFactory

index_page = Blueprint('index_page', __name__, template_folder='/src/view')


@index_page.route('/', methods=['GET'])
def index():
    return render_template('index.html', files=os.listdir(current_app.config['UPLOAD_PATH']))


@index_page.route('/', methods=['POST'])
def upload_files():
    uploaded_file = request.files['file']
    if uploaded_file.filename == '' or os.path.splitext(uploaded_file.filename)[1] not in current_app.config['UPLOAD_EXTENSIONS']:
        return "Invalid file", 400
    filename = os.path.join(
        current_app.config['UPLOAD_PATH'], secure_filename(uploaded_file.filename))
    uploaded_file.save(filename)
    try:
        emotion_scorer = EmotionScorerFactory.create_emotion_scorer(filename)
    except Exception as error:
        current_app.logger.error("Error calculating emotion scores", error)
        return "Invalid file", 400

    @after_this_request
    def remove_file(response):
        try:
            os.remove(filename)
        except Exception as error:
            current_app.logger.error("Error removing upload file", error)
        return response
    return jsonify(indent=2, sort_keys=False, result={"scores": emotion_scorer.scores, "start_times": emotion_scorer.start_times})
