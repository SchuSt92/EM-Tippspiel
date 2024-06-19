from flask import Flask
from flask_admin import Admin
from flask_babel import Babel
from flask_login import LoginManager
from modelviews import *
from db import db

import threading
from datetime import datetime, timedelta
from time import sleep

admin = Admin(index_view=MyAdminIndexView())
babel = Babel()

def create_app():
    # Erstellung der App
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'rt56-4etz-gtz7-rw59-fr64'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    db.init_app(app)

    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin.init_app(app)
    babel.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from models import User, Mannschaft, Spiel, Tipp, Rangliste
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    admin.add_view(UserModelView(User, db.session))
    admin.add_view(MannschaftModelView(Mannschaft, db.session))
    admin.add_view(SpielModelView(Spiel, db.session))
    admin.add_view(TippModelView(Tipp, db.session))
    admin.add_view(RanglisteModelView(Rangliste, db.session))


    #### Hier wird ein Spiel 30 Minuten vor Beginn auf locked gesetzt, damit keine Tipps mehr abgegeben oder geändert werden können.
    ## Achtung auf die Zeitzone des Servers ;D
    # Starte den Hintergrund-Thread
    def lock_spiele():
        while True:
            with app.app_context():
                now = datetime.now()
                thirty_minutes_later = now + timedelta(minutes=30)
                spiele_zum_sperren = Spiel.query.filter(
                    Spiel.datum <= thirty_minutes_later,
                    Spiel.locked == False
                ).all()

                for spiel in spiele_zum_sperren:
                    spiel.locked = True

                db.session.commit()
                # zum Test, kann noch entfernt werden
                print(f"{len(spiele_zum_sperren)} Spiele gesperrt.")
                print(datetime.now())
            # Warte 10 Minuten, bevor du erneut überprüfst
            sleep(600)

    #==== Start des Threads ====
    thread = threading.Thread(target=lock_spiele)
    thread.daemon = True
    thread.start()


    return app