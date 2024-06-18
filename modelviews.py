from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, login_required
from flask import redirect, url_for
from flask_admin import AdminIndexView, expose
from sqlalchemy.testing import db
from models import Tipp, Rangliste
from db import db

# Admin-Ansicht, die nur für Admins (via admin role) zugänglich ist.
class MyAdminIndexView(AdminIndexView):
    @expose('/')
    @login_required
    def index(self):
        # Überprüfen, ob der Benutzer authentifiziert und ein Admin ("admin") ist.
        if not current_user.is_authenticated or current_user.role != 'admin':
            return redirect(url_for('auth.login'))  # Weiterleitung zur Login-Seite, wenn die Überprüfung fehlschlägt.
        return super(MyAdminIndexView, self).index()  # Aufruf der übergeordneten Index-Methode.


"""
# Modell-Ansicht, die nur für authentifizierte Administratoren zugänglich ist.
class MyModelView(ModelView):
    def is_accessible(self):
        # Überprüfen, ob der Benutzer authentifiziert und ein Admin ist.
        return current_user.is_authenticated and current_user.role == 'admin'  # Kleinbuchstaben verwenden

    def inaccessible_callback(self, name, **kwargs):
        # Weiterleitung zur Login-Seite, wenn der Zugriff verweigert wird.
        return redirect(url_for('auth.login'))
"""

class UserModelView(ModelView):
    column_list = ('id', 'email', 'name', 'role')
    form_columns = ('email', 'password', 'name', 'role')


class MannschaftModelView(ModelView):
    column_list = ('id', 'abkuerzung', 'name', 'logo', 'em_titel')
    form_columns = ('abkuerzung', 'name', 'logo', 'em_titel')


class SpielModelView(ModelView):
    column_list = ('id', 'heim_mannschaft', 'gast_mannschaft', 'typ', 'tore_heim', 'tore_gast', 'austragungsort', 'datum', 'gruppe', 'absolviert', 'locked')
    form_columns = ('heim_mannschaft_id', 'gast_mannschaft_id', 'typ', 'tore_heim', 'tore_gast', 'austragungsort', 'datum', 'gruppe', 'absolviert', 'locked')
    column_labels = {
        'heim_mannschaft': 'Heim Mannschaft',
        'gast_mannschaft': 'Gast Mannschaft',
        'tore_heim': 'Tore Heim',
        'tore_gast': 'Tore Gast',
        'austragungsort': 'Austragungsort',
        'datum': 'Datum',
        'gruppe': 'Gruppe',
        'absolviert': 'Absolviert',
        'locked': 'Gesperrt'
    }  # Benutzerdefinierte Labels und Formatierer, um die Anzeige von Daten zu verbessern.
    column_formatters = {
        'gast_mannschaft': lambda v, c, m, p: m.gast_mannschaft.name if m.gast_mannschaft else '',
        'heim_mannschaft': lambda v, c, m, p: m.heim_mannschaft.name if m.heim_mannschaft else ''
    }

    def after_model_change(self, form, model, is_created):
        # Funktion, die nach jeder Änderung an einem Spiel ausgeführt wird, um die Punkte zu berechnen, die jeder Tipper nach dem eintragen des Ergebnisses durch den Admin erhält.
        calculate_scores(model)


class TippModelView(ModelView):
    column_list = ('id', 'user', 'spiel', 'tipp_tore_heim', 'tipp_tore_gast', 'punkte', 'active')  # Spalten, die in der Liste angezeigt werden.
    form_columns = ('user_id', 'spiel_id', 'tipp_tore_heim', 'tipp_tore_gast', 'punkte', 'active')  # Spalten, die im Formular angezeigt werden.
    column_labels = {
        'user': 'User',
        'spiel': 'Spiel',
        'tipp_tore_heim': 'Tipp Tore Heim',
        'tipp_tore_gast': 'Tipp Tore Gast',
        'punkte': 'Punkte',
        'active': 'Aktiv'
    }  # Benutzerdefinierte Labels und Formatierer, um die Anzeige von Daten zu verbessern.
    column_formatters = {
        'user': lambda v, c, m, p: m.user.name if m.user else '',
        'spiel': lambda v, c, m, p: f"{m.spiel.heim_mannschaft.name} vs {m.spiel.gast_mannschaft.name}" if m.spiel else ''
    }

class RanglisteModelView(ModelView):
    column_list = ('id', 'user', 'punkte')
    form_columns = ('user_id', 'punkte')
    column_labels = {
        'user': 'User',
        'punkte': 'Punkte'
    }  # Benutzerdefinierte Labels und Formatierer, um die Anzeige von Daten zu verbessern.
    column_formatters = {
        'user': lambda v, c, m, p: m.user.name if m.user else ''
    }


def calculate_scores(spiel):
    # Überprüfen, ob das Spiel tatsächlich absolviert ist. Wenn nicht, wird die Funktion beendet.
    if not spiel.absolviert:
        return

    # Alle Tipps für das gegebene Spiel aus der Datenbank abfragen.
    tipps = Tipp.query.filter_by(spiel_id=spiel.id).all()

    # Durch alle gefundenen Tipps iterieren.
    for tipp in tipps:
        punkte = 0  # Initiale Punkte für diesen Tipp setzen.

        # Überprüfen, ob der Tipp gültige Tore-Werte enthält.
        if tipp.tipp_tore_gast is None or tipp.tipp_tore_heim is None:
            # 0 Punkte vergeben, wenn die Tore nicht getippt wurden.
            punkte = 0
        else:
            # Überprüfen, ob der Tipp exakt mit dem Spielergebnis übereinstimmt.
            if tipp.tipp_tore_gast == spiel.tore_gast and tipp.tipp_tore_heim == spiel.tore_heim:
                punkte = 3  # 3 Punkte für exakte Übereinstimmung
            # Überprüfen, ob die Tendenz (Heimsieg, Auswärtssieg oder Unentschieden) korrekt ist.
            elif ((tipp.tipp_tore_gast > tipp.tipp_tore_heim) and (spiel.tore_gast > spiel.tore_heim)) or \
                 ((tipp.tipp_tore_gast < tipp.tipp_tore_heim) and (spiel.tore_heim > spiel.tore_gast)) or \
                 ((tipp.tipp_tore_gast == tipp.tipp_tore_heim) and (spiel.tore_gast == spiel.tore_heim)):
                punkte = 1  # 1 Punkt für korrekte Tendenz

        # Die berechneten Punkte im Tipp speichern.
        tipp.punkte = punkte
        db.session.add(tipp)

        # Den Ranglisteneintrag für den Benutzer dieses Tipps abfragen.
        rangliste = Rangliste.query.filter_by(user_id=tipp.user_id).first()

        # Wenn ein Ranglisteneintrag existiert, die Punkte aktualisieren.
        if rangliste:
            rangliste.punkte += punkte
        else:
            # Wenn kein Ranglisteneintrag existiert, einen neuen Eintrag erstellen.
            rangliste = Rangliste(user_id=tipp.user_id, punkte=punkte)

        # Den aktualisierten oder neuen Ranglisteneintrag zur Sitzung hinzufügen.
        db.session.add(rangliste)

    # Alle Änderungen in der Datenbank speichern.
    db.session.commit()
