from flask import Flask
from db import db

def create_app():
    # Erstellung der App
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'rt56-4etz-gtz7-rw59-fr64'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    db.init_app(app)

    from auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
