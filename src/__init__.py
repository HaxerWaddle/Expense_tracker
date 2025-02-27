from flask import Flask
from src.config import Config
from src.models import db, login_manager

app = Flask(__name__)
app.config.from_object(Config)


db.init_app(app)
login_manager.init_app(app)

with app.app_context():
    db.create_all()

from src import routes