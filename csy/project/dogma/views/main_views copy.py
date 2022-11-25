# from werkzeug.utils import redirect

# from flask import Blueprint, Flask, render_template, request, session
# # from keras.models import load_model
# from keras.preprocessing import image
# # from keras import utils

# # import numpy as np
# from datetime import datetime
# import os

# from dogma.models import Imginfo
# from dogma import db

# # img_dir = os.listdir('dogma/static/images')

# # dic = {0: '정상', 1: '불량'}

# # model = load_model('dogma/static/cnn_3.h5')

# # model.make_predict_function()

# now = datetime.now()

# # date_str = now.strftime('%y%m%d-%H:%M:%S')

# # def predict_label(img_path):
# #     print(img_path)
# #     test_img = utils.load_img(img_path, color_mode='grayscale', target_size=(256, 256), interpolation='bilinear')
# #     x = utils.img_to_array(test_img)
# #     x = np.expand_dims(x, axis=0)
# #     images = np.vstack([x])

# #     p = model.predict(images, batch_size=16)

# #     tmp = p.tolist()
# #     return dic[tmp[0][0]]

# bp = Blueprint('main', __name__, url_prefix='/main')

# @bp.route('/', methods=['GET', 'POST'])
# def main():
#     imginfo_list = Imginfo.query.order_by(Imginfo.predictdate.asc())
#     return render_template('main/main.html', imginfo_list=imginfo_list)

# # @bp.route('/submit/', methods=['GET', 'POST'])
# # def predict():
# #     print('DEBUG1')
# #     if request.method == 'POST':
# #         global pred, img_path, img_path_name

# #         img = request.files['my_image']
# #         # img_dir_path = os.path.join('dogma/static/images','img.filename')

# #         # if os.path.isfile(img_dir_path) == True:
# #             # pass
# #         # else:
# #         img_path_name = 'images/' + img.filename
# #         new_file_name = "img_" + now.strftime("%y.%m.%d-%H：%M：%S.%f") + '_' + img.filename
# #         img_path = "dogma/static/images/" + new_file_name
# #         img.save(img_path)

# #         pred = predict_label(img_path)

# #         # db_img_filename = os.rename(img.filename, 'img_'+img.filename+datetime.now())
# #         # img_dir_path = "dogma/static/images/"
# #         # old_name = img_path
# #         # new_name = img_dir_path + "img_" + str(now.strftime('%y%m%d-%H:%M:%S')) + '_' + img.filename
# #         # new_name = img_dir_path + "img_" + str(datetime.today()) + '_' + img.filename
# #         # new_file_name = "img_" + str(datetime.today()) + img.filename
# #         # render_img_path = 'images/' + new_file_name
# #         # new_img_name = os.rename(old_name, new_name)
# #         # print(new_img_name)

# #         # new_file_name = "img_" + (datetime.now()-timedelta(microseconds=266019)).strftime("%y%m%d-%H.%M.%S.%f") + '_' + img.filename
# #         render_img_path = 'images/' + new_file_name
    
# #         img_info = Imginfo(imgname=new_file_name, predictdate=now, prediction=pred)
        
        
# #         db.session.add(img_info)
# #         db.session.commit()
        
# #         imginfo_list = Imginfo.query.order_by(Imginfo.predictdate.asc())

# #         print("@@@DEBUG2@@@", session["csrf_token"])

# #     return render_template('main/main.html', prediction = pred, img_path = img_path, img_name=render_img_path, imginfo_list=imginfo_list)