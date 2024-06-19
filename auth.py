from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, Spiel, Tipp, Rangliste
from __init__ import db
from flask_login import login_user, logout_user, login_required, current_user

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
#Regestrierung und Erstellung von den benötigten DB-Einträgen für einen Nutzer. (z.B. Tipps, Account etc.)
@auth.route('/registrieren', methods=["POST"])
def registrieren_post():
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        confirm_password = request.form.get('confirmPassword')


        if not email or not name or not password or not confirm_password:
            flash('Bitte alle Felder ausfüllen!')
            return redirect(url_for('auth.registrieren'))
        if password != confirm_password:
            flash('Die Passwörter stimmen nicht überein!')
            return redirect(url_for('auth.registrieren'))

        user = User.query.filter_by(
            email=email).first()  # if this returns a user, then the email already exists in database
        if user:  # if a user is found, we want to redirect back to signup page so user can try again
            flash('Email address already exists')
            return redirect(url_for('auth.registrieren'))

        verifyName = User.query.filter_by(name=name).first()
        if verifyName:  # if a user is found, we want to redirect back to signup page so user can try again
            flash('Name address already exists')
            return redirect(url_for('auth.registrieren'))


        # create a new user with the form data. Hash the password so the plaintext version isn't saved.
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        new_user = User(email=email, name=name, password=hashed_password, role="user")

        # add the new user to the database
        try:
            db.session.add(new_user)
            db.session.commit()
            # Fetch all games from the database
            spiele = Spiel.query.all()

            # Create a Tipp for each game for the new user
            for spiel in spiele:
                new_tipp = Tipp(
                    user_id=new_user.id,
                    spiel_id=spiel.id,
                    tipp_tore_gast=None,  # Set these to None initially
                    tipp_tore_heim=None,  # Set these to None initially
                    punkte=0
                )
                db.session.add(new_tipp)

            new_rangliste = Rangliste(
                user_id=new_user.id,
                punkte=0
            )
            db.session.add(new_rangliste)

            db.session.commit()

            flash('Account created successfully!')
            return redirect(url_for('auth.login'))

        except Exception as e:
            db.session.rollback()
            flash(f'Error creating account: {e}')
            return redirect(url_for('auth.registrieren'))



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
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False
    user = User.query.filter_by(email=email).first()

    # Passwortüberprüfung
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(
            url_for('auth.login'))  # falls Benutzer nicht existiert oder Passwort falsch ist, Seite neu laden

    # Falls die Überprüfung erfolgreich ist, Benutzer zur Profilseite weiterleiten
    login_user(user, remember=remember)
    print(f'Logged in user role: {user.role}')
    return redirect(url_for('auth.profil'))



@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@auth.route('/tipps', methods=["GET"])
@login_required
def tipps_get():
    next_game = get_next_game()
    # Spiele abrufen
    spiele = Spiel.query.order_by(Spiel.gruppe, Spiel.datum).all()
    # Tipps des angemeldeten Benutzers abrufen
    tipps = Tipp.query.filter_by(user_id=current_user.id).all()

    # Tipps in einem Dictionary speichern, um schnellen Zugriff zu ermöglichen
    tipps_dict = {tipp.spiel_id: tipp for tipp in tipps}

    data = {}
    for spiel in spiele:
        if spiel.gruppe not in data:
            data[spiel.gruppe] = []
        # Tipps zu den Spielen hinzufügen
        spiel_tipps = tipps_dict.get(spiel.id, None)
        data[spiel.gruppe].append({
            'spiel': spiel,
            'tipp': spiel_tipps
        })

    return render_template("tipps.html",
                           heimMannschaft=next_game['heim_mannschaft'],
                           auswaertsMannschaft=next_game['auswaerts_mannschaft'],
                           datum=next_game['datum'],
                           logoHeim=next_game['logo_heim'],
                           logoAuswaerts=next_game['logo_auswaerts'],
                           data=data)


#Übermittelung der Tipps des Users
@auth.route('/tipps', methods=["POST"])
@login_required
def tipps_post():
    form_data = request.form

    # Debugging-Ausgabe für empfangene Formulardaten
    print("Empfangene Formulardaten:", form_data)

    for key, value in form_data.items():
        if 'game' in key:
            # Extrahiere die Spiel-ID und das Team (heim/auswärts) aus dem Feldnamen
            parts = key.split('_')
            spiel_id = int(parts[0][4:])  # Extrahiere die Spiel-ID aus game<ID>_team<X>
            team_type = parts[1]

            # Debugging-Ausgabe für jedes Eingabefeld
            print(f"Verarbeite {key}: {value}")

            # Überprüfen, ob das Spiel locked ist
            spiel = Spiel.query.get(spiel_id)
            if spiel and spiel.locked:
                print(f"Spiel {spiel_id} ist gesperrt.")
                continue

            # Überprüfen, ob der aktuelle Benutzer bereits einen Tipp für dieses Spiel abgegeben hat
            tipp = Tipp.query.filter_by(user_id=current_user.id, spiel_id=spiel_id).first()
            if tipp:
                # Validierung: Stellen Sie sicher, dass value eine positive ganze Zahl ist
                if value.isdigit():
                    value_int = int(value)
                    if value_int >= 0:
                        if team_type == 'team1':
                            tipp.tipp_tore_heim = value_int
                        elif team_type == 'team2':
                            tipp.tipp_tore_gast = value_int
                        print(f"Tipp für Spiel {spiel_id} gesetzt: Heim {tipp.tipp_tore_heim}, Gast {tipp.tipp_tore_gast}")

                        # Setze active auf True, da ein Wert übermittelt wurde
                        tipp.active = True
                    else:
                        flash(f"Ungültiger Wert für {key}. Bitte geben Sie eine positive ganze Zahl ein.", "error")
                        return redirect(url_for('auth.tipps_get'))
                else:
                    if value == "":
                        # Wenn das Eingabefeld leer ist, setze den Wert auf None
                        if team_type == 'team1':
                            tipp.tipp_tore_heim = None
                        elif team_type == 'team2':
                            tipp.tipp_tore_gast = None
                        print(f"Tipp für Spiel {spiel_id} gesetzt: Heim {tipp.tipp_tore_heim}, Gast {tipp.tipp_tore_gast} (leer)")
                    else:
                        flash(f"Ungültiger Wert für {key}. Bitte geben Sie eine positive ganze Zahl ein.", "error")
                        return redirect(url_for('auth.tipps_get'))

                # Füge den Tipp zur Sitzung hinzu
                db.session.add(tipp)
            else:
                print(f"Kein Tipp für Spiel {spiel_id} gefunden.")

    # Änderungen in der Datenbank speichern
    try:
        db.session.commit()
        print("Änderungen in der Datenbank gespeichert.")
    except Exception as e:
        db.session.rollback()
        print(f"Fehler beim Speichern der Änderungen: {e}")
        flash(f"Fehler beim Speichern der Änderungen: {e}", "error")
        return redirect(url_for('auth.tipps_get'))

    # Ausnahmebehandlungen: Setze Tore auf 0, wenn nur für eine Mannschaft getippt wurde
    for tipp in Tipp.query.filter_by(user_id=current_user.id).all():
        if tipp.active:
            if tipp.tipp_tore_heim is None and tipp.tipp_tore_gast is not None:
                tipp.tipp_tore_heim = 0
            elif tipp.tipp_tore_gast is None and tipp.tipp_tore_heim is not None:
                tipp.tipp_tipp_tore_gast = 0
            print(f"Tore für Spiel {tipp.spiel_id} auf 0 gesetzt: Heim {tipp.tipp_tore_heim}, Gast {tipp.tipp_tore_gast}")

            # Füge den Tipp zur Sitzung hinzu
            db.session.add(tipp)

    # Änderungen in der Datenbank speichern
    try:
        db.session.commit()
        print("Änderungen in der Datenbank gespeichert.")
    except Exception as e:
        db.session.rollback()
        print(f"Fehler beim Speichern der Änderungen: {e}")
        flash(f"Fehler beim Speichern der Änderungen: {e}", "error")
        return redirect(url_for('auth.tipps_get'))

    flash("Deine Tipps wurden erfolgreich gespeichert.", "success")

    # Leite den Benutzer zur Tipps-Seite zurück
    return redirect(url_for('auth.tipps_get'))






@auth.route("/profil", methods=["GET"])
@login_required
def profil():
        next_game = get_next_game()

        # Rangliste abfragen und nach Punkten sortieren
        rangliste = Rangliste.query.order_by(Rangliste.punkte.desc()).all()

        # Bestimmen der Position und Punkte des aktuellen Benutzers
        user_position = 0;
        user_points = 6

        # Debugging-Ausgabe: Ausgabe der Rangliste
        for entry in rangliste:
            print(f"User ID: {entry.user_id}, Punkte: {entry.punkte}")

        for i in range(len(rangliste)):
            if rangliste[i].user_id == current_user.id:
                user_position = i + 1
                user_points = rangliste[i].punkte
                break

            # Debugging-Ausgabe: Überprüfen, ob der Benutzer gefunden wurde
            print(f"Benutzer gefunden: {current_user.id}, Position: {user_position}, Punkte: {user_points}")

        return render_template('profil.html',
                                heimMannschaft=next_game['heim_mannschaft'],
                                auswaertsMannschaft=next_game['auswaerts_mannschaft'],
                                datum=next_game['datum'],
                                logoHeim=next_game['logo_heim'],
                                logoAuswaerts=next_game['logo_auswaerts'],
                                rangliste=rangliste,
                                name=current_user.name,
                                email=current_user.email,
                                user_position=user_position,
                                user_points=user_points)



# Vielleicht noch ausglieder da doppelt verwendet
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