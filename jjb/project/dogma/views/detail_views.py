from flask import Blueprint, render_template


from dogma.models import Imginfo

bp = Blueprint('detail', __name__, url_prefix='/detail')


@bp.route('/<int:imginfo_id>/', methods=['GET'])
def detail(imginfo_id):
    global imginfo
    imginfo = Imginfo.query.get(imginfo_id)
    img_path = "images/" + imginfo.imgname

    return render_template('detail.html', imginfo=imginfo, img_path = img_path)