from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, request, flash
from models import User, Spiel, Tipp, Rangliste

# Blueprint für alle Seiten für die eine Authentifizierung notwendig ist.
# https://flask.palletsprojects.com/en/3.0.x/blueprints/
auth = Blueprint('auth', __name__)


@auth.route('/registrieren', methods=["GET"])
def registrieren():
    next_game = get_next_game()
    return render_template("registrieren.html",
                           heimMannschaft=next_game['heim_mannschaft'],
                           auswaertsMannschaft=next_game['auswaerts_mannschaft'],
                           datum=next_game['datum'],
                           logoHeim=next_game['logo_heim'],
                           logoAuswaerts=next_game['logo_auswaerts'])


# Übermittelung der Formular Daten
#Regestrierung und Erstellung von den benötigten DB-Einträgen für einen Nutzer. (z.B. Tipps, Account etc.
# )
@auth.route('/registrieren', methods=["POST"])
def registrieren_post():
    return "Registrieren - POST"



@auth.route('/login', methods=["GET"])
def login():
    next_game = get_next_game()
    return render_template('login.html',
                           heimMannschaft=next_game['heim_mannschaft'],
                           auswaertsMannschaft=next_game['auswaerts_mannschaft'],
                           datum=next_game['datum'],
                           logoHeim=next_game['logo_heim'],
                           logoAuswaerts=next_game['logo_auswaerts'])


@auth.route('/login', methods=['POST'])
def login_post():
    return "Login - POST"


@auth.route('/logout')
def logout():
    return "Logout"


@auth.route('/tipps', methods=["GET"])
def tipps_get():
    return "Tipps"


#Übermittelung der Tipps des Users
@auth.route('/tipps', methods=["POST"])
def tipps_post():
    return "Tipps - POST"

@auth.route("/profil", methods=["GET"])
def home():
    return "Home - Info"




def get_next_game():
    # Aktuelles Datum und Uhrzeit abrufen
    now = datetime.now()
    # Alle Spiele aus der Datenbank abfragen, die nach dem aktuellen Datum liegen
    upcoming_spiele = Spiel.query.filter(Spiel.datum > now).order_by(Spiel.datum).all()

    # Das nächstliegende Spiel finden
    if upcoming_spiele:
        naechstes_spiel = upcoming_spiele[0]
        heim_mannschaft = naechstes_spiel.heim_mannschaft.name
        auswaerts_mannschaft = naechstes_spiel.gast_mannschaft.name
        datum = naechstes_spiel.datum.strftime("%d. %B %Y, %H:%M Uhr")
        logo_heim = naechstes_spiel.heim_mannschaft.logo
        logo_auswaerts = naechstes_spiel.gast_mannschaft.logo
    else:
        heim_mannschaft = "Keine"
        auswaerts_mannschaft = "Keine"
        datum = "Kein Spiel geplant"
        logo_heim = "static/pictures/placeholder.png"
        logo_auswaerts = "static/pictures/placeholder.png"

    return {
        'heim_mannschaft': heim_mannschaft,
        'auswaerts_mannschaft': auswaerts_mannschaft,
        'datum': datum,
        'logo_heim': logo_heim,
        'logo_auswaerts': logo_auswaerts
    }