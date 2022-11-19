from werkzeug.utils import redirect

from flask import Blueprint, Flask, render_template, request, session, abort, url_for
from keras.models import load_model
from keras.preprocessing import image
from keras import utils

import numpy as np
from datetime import datetime
import os

from dogma.models import Imginfo
from dogma import db

from dogma.forms import UserCreateForm, UserLoginForm
# img_dir = os.listdir('dogma/static/images')

dic = {0: '정상', 1: '불량'}

model = load_model('dogma/static/cnn_3.h5')

model.make_predict_function()

def predict_label(img_path):
    test_img = utils.load_img(img_path, color_mode='grayscale', target_size=(256, 256), interpolation='bilinear')
    x = utils.img_to_array(test_img)
    x = np.expand_dims(x, axis=0)
    images = np.vstack([x])

    p = model.predict(images, batch_size=16)

    tmp = p.tolist()
    return dic[tmp[0][0]]

bp = Blueprint('main', __name__, url_prefix='/main')

def login_is_required():
    
    if "google_id" not in session:
        session.clear()
        return False

    else:
        return True


@bp.route('/', methods=['GET', 'POST'])
def main():
    imginfo_list = Imginfo.query.order_by(Imginfo.predictdate.asc())
    return render_template('main/main.html', imginfo_list=imginfo_list, isSession=login_is_required())

@bp.route('/submit/', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        global pred, img_path, img_path_name

        img = request.files['my_image']
        # img_dir_path = os.path.join('dogma/static/images','img.filename')

        # if os.path.isfile(img_dir_path) == True:
            # pass
        # else:
        img_path_name = 'images/' + img.filename
        img_path = "dogma/static/images/" + img.filename
        img.save(img_path)

        pred = predict_label(img_path)

        img_info = Imginfo(imgname=img.filename, predictdate=datetime.now(), prediction=pred)
        
        
        db.session.add(img_info)
        db.session.commit()
        
        imginfo_list = Imginfo.query.order_by(Imginfo.predictdate.asc())

        print("@@@DEBUG2@@@", session["csrf_token"])

    return render_template('main/main.html', prediction = pred, img_path = img_path, img_name=img_path_name, imginfo_list=imginfo_list)