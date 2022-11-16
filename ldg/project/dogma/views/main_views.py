from werkzeug.utils import redirect

from flask import Blueprint, Flask, render_template, request
from keras.models import load_model
from keras.preprocessing import image
from keras import utils

import numpy as np

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

@bp.route('/', methods=['GET', 'POST'])
def main():
    return render_template('main/main.html')

@bp.route('/submit/', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        global pred
        global img_path
        img = request.files['my_image']

        img_path = "dogma/images/" + img.filename
        img.save(img_path)

        pred = predict_label(img_path)

    return render_template('main/main.html', prediction = pred, img_path = img_path)