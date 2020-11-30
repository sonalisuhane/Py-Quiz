from flask import Flask,url_for
#from config import TestConfig
from config import Config
from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate
from flask_login import LoginManager 
from flask_admin.menu import MenuLink
from flask_admin import Admin, expose, AdminIndexView
from flask_bootstrap import Bootstrap
from flask_admin.contrib.sqla import ModelView


app = Flask(__name__)
db = SQLAlchemy(app)
app.config.from_object(Config)
#app.config.from_object(TestConfig)
Bootstrap(app)
migrate = Migrate(app, db)

admin = Admin(app, name='Dash Board', template_mode='bootstrap3')

login = LoginManager(app)
login.login_view = 'login'

from app.models import User,Question,feedback,Result,MCQ,answers
admin.add_link(MenuLink(name='Main Menu', url='/'))
admin.add_view(ModelView(User,db.session))
admin.add_view(ModelView(Question,db.session))
admin.add_view(ModelView(MCQ, db.session))
admin.add_view(ModelView(answers, db.session))
admin.add_view(ModelView(Result,db.session))
admin.add_view(ModelView(feedback,db.session))

db.create_all()
from app import routes, models