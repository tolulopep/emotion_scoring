from flask import Blueprint

error_page = Blueprint('error_page', __name__, template_folder='/src/view')

@error_page.errorhandler(413)
def too_large(e):
    return "File is too large", 413