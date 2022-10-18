from flask_sqlalchemy import SQLAlchemy


db = {
    'user'      : 'root',
    'password'  : '1234',
    'host'      : '127.0.0.1',
    'port'      : '3306',
    'database'  : 'inputdata'
}

SQLALCHEMY_DATABASE_URI = f"mysql+mysqlconnector://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['database']}?charset=utf8"
SQLALCHEMY_TRACK_MODIFICATIONS = False