from flask import Blueprint, Flask, render_template, flash, request, session, abort
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect

from dogma.models import User

bp = Blueprint('main', __name__, url_prefix='/main')

@bp.route('/')
def main():
    return render_template('main/main.html')