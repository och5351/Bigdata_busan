from flask import Blueprint, Flask, render_template

from pybo.models import User

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/hello')
def hello_dogma():
    return 'Hello, Dogma!'

@bp.route('/')
def index():
    return 'Dogma index'