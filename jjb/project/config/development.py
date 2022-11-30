from flask_sqlalchemy import SQLAlchemy

db = {
    'user'      : 'sixdogma',
    'password'  : 'Poiu0987*',
    'host'      : '13.113.12.130',
    'port'      : '3306',
    'database'  : 'Flask'
}

SQLALCHEMY_DATABASE_URI = f"mysql+mysqlconnector://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['database']}?charset=utf8"
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = "dev"