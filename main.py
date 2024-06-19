from datetime import datetime
from models import Spiel, Rangliste
from flask import Blueprint, render_template

main = Blueprint("main", __name__)

@main.route("/", methods=["GET"])
def index():
    next_game = get_next_game()
    # Rangliste abfragen und nach Punkten sortieren
    rangliste = Rangliste.query.order_by(Rangliste.punkte.desc()).limit(10).all()
    return render_template("home.html",
                           heimMannschaft=next_game['heim_mannschaft'],
                           auswaertsMannschaft=next_game['auswaerts_mannschaft'],
                           datum=next_game['datum'],
                           logoHeim=next_game['logo_heim'],
                           logoAuswaerts=next_game['logo_auswaerts'],
                           rangliste=rangliste)

@main.route("/rangliste", methods=["GET"])
def rangliste():
    next_game = get_next_game()
    rangliste = Rangliste.query.order_by(Rangliste.punkte.desc()).limit(100).all()

    return render_template("rangliste.html",
                           heimMannschaft=next_game['heim_mannschaft'],
                           auswaertsMannschaft=next_game['auswaerts_mannschaft'],
                           datum=next_game['datum'],
                           logoHeim=next_game['logo_heim'],
                           logoAuswaerts=next_game['logo_auswaerts'],
                           rangliste=rangliste)


@main.route("/info", methods=["GET"])
def info():
    next_game = get_next_game()
    return render_template("info.html",
                           heimMannschaft=next_game['heim_mannschaft'],
                           auswaertsMannschaft=next_game['auswaerts_mannschaft'],
                           datum=next_game['datum'],
                           logoHeim=next_game['logo_heim'],
                           logoAuswaerts=next_game['logo_auswaerts'])



@main.route("/spielplan", methods=["GET"])
def spielplan():
    # Debugging user information
    print("Accessing the spielplan route")
    next_game = get_next_game()
    spiele = Spiel.query.order_by(Spiel.gruppe, Spiel.datum).all()
    data = {}

    for spiel in spiele:
        print(f"Processing game: {spiel.id}, Group: {spiel.gruppe}")
        if spiel.gruppe not in data:
            data[spiel.gruppe] = []
        data[spiel.gruppe].append(spiel)

    return render_template('spielplan.html',
                           heimMannschaft=next_game['heim_mannschaft'],
                           auswaertsMannschaft=next_game['auswaerts_mannschaft'],
                           datum=next_game['datum'],
                           logoHeim=next_game['logo_heim'],
                           logoAuswaerts=next_game['logo_auswaerts'],
                           rangliste=next_game,
                           data=data)




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