from flask_sqlalchemy import SQLAlchemy

db = {
    'user'      : 'dogma',
    'password'  : 'Dogma7789!',
    'host'      : '54.180.131.194',
    'port'      : '3306',
    'database'  : 'auth'
}

SQLALCHEMY_DATABASE_URI = f"mysql+mysqlconnector://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['database']}?charset=utf8"
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = "dev"