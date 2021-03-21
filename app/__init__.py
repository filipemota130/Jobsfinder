import logging
from logging.handlers import RotatingFileHandler
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)
migrate= Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

login_manager = LoginManager()
login_manager.init_app(app)
if not app.debug:
    if not os.path.exists("logs"):
        os.mkdir("logs")
    arquivo_handler = RotatingFileHandler("logs/erros.log", maxBytes=1000000, backupCount=10)
    arquivo_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s: %(message)s [em %(pathname)s:%(lineno)d]"))
    arquivo_handler.setLevel(logging.WARNING)
    app.logger.addHandler(arquivo_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info("Aplicação inicializada!")

from app.models import user, job , forms
from app.templates import *
from app.controllers import router