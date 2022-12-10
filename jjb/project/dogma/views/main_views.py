# from werkzeug.utils import redirect

from flask import Blueprint, Flask, render_template, request, session, abort, url_for
# from keras.models import load_model
# from keras.preprocessing import image
# from keras import utils

# import numpy as np
# from datetime import datetime
# import os

from dogma.models import Imginfo
# from dogma import db

# from dogma.forms import UserCreateForm, UserLoginForm
# img_dir = os.listdir('dogma/static/images')

def login_is_required():
    if "google_id" not in session:
        session.clear()
        return False
    else:
        return True

def login_is_required2():
    if "user_id" not in session:
        session.clear()
        return False
    else:
        return True

bp = Blueprint('main', __name__, url_prefix='/main')


@bp.route('/', methods=['GET', 'POST'])
def main():
    if "google_id" in session:
        imginfo_list = Imginfo.query.order_by(Imginfo.predictdate.asc())
        print("@@@DEBUG2@@@", session)
        return render_template('main/main.html', imginfo_list=imginfo_list, isSession=login_is_required())
    
    elif "user_id" in session:
        imginfo_list = Imginfo.query.order_by(Imginfo.predictdate.asc())
        print("@@@DEBUG2@@@", session)
        return render_template('main/main.html', imginfo_list=imginfo_list, isSession=login_is_required2())
