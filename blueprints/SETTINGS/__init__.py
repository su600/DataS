from flask import Blueprint

settings_ = Blueprint('settings_', __name__,template_folder="login_page", url_prefix="/login")

from . import views