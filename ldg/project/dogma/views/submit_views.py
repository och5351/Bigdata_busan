from flask import Blueprint, Flask, render_template, request, session

from keras import utils
from keras.models import load_model

from dogma.models import Imginfo,Imginfo2
from dogma import db

import numpy as np
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("apachehive:///?Server=13.125.214.72&Port=10000&TransportMode=BINARY")
factory = sessionmaker(bind=engine)
session = factory()

dic = {0: '정상', 1: '불량'}

# 기존 모델 로드
# model = load_model('dogma/static/cnn_3.h5')

# 재훈련된 모델 로드
model = load_model('dogma/static/cnn_padding.h5')

model.make_predict_function()

now = datetime.now()

def predict_label(img_path):
    test_img = utils.load_img(img_path, color_mode='grayscale', target_size=(256, 256), interpolation='bilinear')
    x = utils.img_to_array(test_img)
    x = np.expand_dims(x, axis=0)
    images = np.vstack([x])

    p = model.predict(images, batch_size=16)

    tmp = p.tolist()
    return dic[tmp[0][0]]

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

bp = Blueprint('submit', __name__, url_prefix='/main')

@bp.route('/submit/', methods=['GET', 'POST'], strict_slashes=False)
def predict():
    if "google_id" in session:
        if request.method == 'POST':
            global pred, img_path, img_path_name

            try:
                img = request.files['my_image']
                img_path_name = 'images/' + img.filename
                new_file_name = "img_" + datetime.now().strftime("%y.%m.%d-%H：%M：%S.%f") + '_' + img.filename
                img_path = "dogma/static/images/" + new_file_name
                img.save(img_path)

                pred = predict_label(img_path)

                if pred == "정상":
                    img.save("dogma/static/images/good/" + new_file_name)
                else:
                    img.save("dogma/static/images/bad/" + new_file_name)
                render_img_path = 'images/' + new_file_name

                # img_info = Imginfo(imgname=new_file_name, predictdate=now, prediction=pred)
                
                img_info = Imginfo2(imgname=new_file_name, predictdate=now, prediction=pred)

                session.add(img_info)
                session.commit()
            
                # db.session.add(img_info)
                # db.session.commit()
                
                imginfo_list = Imginfo.query.order_by(Imginfo.predictdate.asc())

            # print("@@@DEBUG2@@@", session["csrf_token"])

                return render_template('main/submit.html', prediction = pred, img_path = img_path, img_name=render_img_path, imginfo_list=imginfo_list, isSession=login_is_required())
            except:
                imginfo_list = Imginfo.query.order_by(Imginfo.predictdate.asc())
                return render_template('main/main.html',imginfo_list=imginfo_list, isSession=login_is_required())
    elif "user_id" in session:
        if request.method == 'POST':
            try:
                img = request.files['my_image']
                img_path_name = 'images/' + img.filename
                new_file_name = "img_" + datetime.now().strftime("%y.%m.%d-%H：%M：%S.%f") + '_' + img.filename
                img_path = "dogma/static/images/" + new_file_name
                img.save(img_path)

                pred = predict_label(img_path)

                if pred == "정상":
                    img.save("dogma/static/images/good/" + new_file_name)
                else:
                    img.save("dogma/static/images/bad/" + new_file_name)
                render_img_path = 'images/' + new_file_name

                img_info = Imginfo(imgname=new_file_name, predictdate=now, prediction=pred)
                
                
                db.session.add(img_info)
                db.session.commit()
                
                imginfo_list = Imginfo.query.order_by(Imginfo.predictdate.asc())

                return render_template('main/submit.html', prediction = pred, img_path = img_path, img_name=render_img_path, imginfo_list=imginfo_list, isSession=login_is_required2())
            except:
                imginfo_list = Imginfo.query.order_by(Imginfo.predictdate.asc())
                return render_template('main/main.html', imginfo_list=imginfo_list, isSession=login_is_required2())