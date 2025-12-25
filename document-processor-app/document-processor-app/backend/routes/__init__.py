from flask import Blueprint

routes = Blueprint('routes', __name__)

from .upload import *  # Import all routes from upload.py