from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

app.config['SECRET_KEY'] = 'd5cc81572eff069d9869ec84588aaa70'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:notiene@localhost/buscolegio'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from buscolegio import routes