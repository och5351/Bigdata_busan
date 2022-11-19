from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

import config

db = SQLAlchemy()
migrate = Migrate()

def create_app():   # app 실행 함수
    app = Flask(__name__)
    app.config.from_envvar('APP_CONFIG_FILE')

    # ORM
    db.init_app(app)
    migrate.init_app(app, db)
    from . import models

    # 블루프린트
    from .views import main_views, auth_views, oauth_views
    app.register_blueprint(auth_views.bp)
    app.register_blueprint(main_views.bp)
    app.register_blueprint(oauth_views.bp)

    return app