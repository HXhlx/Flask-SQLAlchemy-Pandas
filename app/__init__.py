from flask import Flask

from app.auth import auth
from app.home import home
from app.models import db

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://@localhost/Demo?driver=ODBC Driver 17 for SQL Server;Trusted_Connection=yes'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Demo.db'
app.config['SECRET_KEY'] = 'dev'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db.init_app(app)
app.register_blueprint(auth)
app.register_blueprint(home)
