from flask import Blueprint, Flask, render_template, flash, request, session, url_for, g
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect

from dogma import db
from dogma.forms import UserCreateForm, UserLoginForm
from dogma.models import User


bp = Blueprint('auth', __name__, url_prefix='/')

@bp.route('/signup/', methods=('GET', 'POST'))
def signup():
    form = UserCreateForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            user = User(username=form.username.data,
                        password=generate_password_hash(form.password1.data),
<<<<<<< Updated upstream
                        email=form.email.data)
=======
                        email=form.email.data,
                        userid=form.userid.data,
                        number=form.number.data,
                        )
            # 여기에 model과 같게 추가
>>>>>>> Stashed changes
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('auth.login'))
        else:
            flash('이미 존재하는 사용자입니다.')
<<<<<<< Updated upstream
    return render_template('bootstrap/signup.html', form=form)
=======
    return render_template('auth/signup.html', form=form)
>>>>>>> Stashed changes


@bp.route('/', methods=('GET', 'POST'))
def login():
    form = UserLoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        error = None
<<<<<<< Updated upstream
        user = User.query.filter_by(username=form.username.data).first()
=======
        user = User.query.filter_by(userid=form.userid.data).first()
>>>>>>> Stashed changes
        if not user:
            error = "존재하지 않는 사용자입니다."
        elif not check_password_hash(user.password, form.password.data):
            error = "비밀번호가 올바르지 않습니다."
        if error is None:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('main.main'))
        flash(error)
<<<<<<< Updated upstream
    return render_template('bootstrap/login.html', form=form)
=======
    return render_template('auth/login.html', form=form)
>>>>>>> Stashed changes

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)

@bp.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))