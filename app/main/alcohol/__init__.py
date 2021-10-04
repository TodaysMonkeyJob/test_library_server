from flask import Blueprint

alcohol = Blueprint('alcohol', __name__, url_prefix='/alcohols',template_folder='templates')

from . import views
