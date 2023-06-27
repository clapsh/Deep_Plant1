from flask import Blueprint
#from .views import *

auth = Blueprint('auth', __name__, static_folder="static", template_folder="templates", static_url_path='static')

from .views import *