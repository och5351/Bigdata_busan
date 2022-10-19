from flask import Blueprint, Flask, render_template, flash, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect

from dogma.models import User

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/')
def hello():
    return render_template('main/main.html')