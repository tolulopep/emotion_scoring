import os
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, jsonify, after_this_request, Blueprint, current_app
from src.model.factory.emotion_scorer_factory import create_emotion_scorer

index_page = Blueprint('index_page', __name__, template_folder='/src/view')


@index_page.route('/', methods=['GET'])
def index():
    '''
    Shows welcome page
    '''
    return render_template('index.html')


@index_page.route('/', methods=['POST'])
def upload_file():
    '''
    Calculates and returns emotion scores from an uploaded file using the right emotion scorer. 
    Parameters:
      file (byte): Uploaded file. Must have an extension in the UPLOAD_EXTENSIONS extension
    Returns:
      json: Json containing scores (key value of labels with their appropriate emotion ranking for each caption) and start_times (list of the start times of each caption)
    '''
    uploaded_file = request.files['file']
    if uploaded_file.filename == '' or os.path.splitext(uploaded_file.filename)[1] not in current_app.config['UPLOAD_EXTENSIONS']:
        return "Invalid file", 400
    filename = os.path.join(
        current_app.config['UPLOAD_PATH'], secure_filename(uploaded_file.filename))
    uploaded_file.save(filename)
    try:
        emotion_scorer = create_emotion_scorer(filename)
    except Exception as error:
        current_app.logger.error("Error calculating emotion scores", error)
        return "Invalid file", 400

    @after_this_request
    def remove_file(response):
        '''
        Deletes uploaded file after processing
        '''
        try:
            os.remove(filename)
        except Exception as error:
            current_app.logger.error("Error removing upload file", error)
        return response
    return jsonify(indent=2, sort_keys=False, result={"scores": emotion_scorer.scores, "start_times": emotion_scorer.start_times})
