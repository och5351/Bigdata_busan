# from werkzeug.utils import redirect

from flask import Blueprint, Flask, render_template, request, session
# from keras.preprocessing import image

from dogma.models import Imginfo

bp = Blueprint('main', __name__, url_prefix='/main')

@bp.route('/', methods=['GET', 'POST'])
def main():
    imginfo_list = Imginfo.query.order_by(Imginfo.predictdate.asc())
    return render_template('main/main.html', imginfo_list=imginfo_list)