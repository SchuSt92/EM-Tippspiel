from datetime import datetime
from werkzeug.security import generate_password_hash
from __init__ import db
from run import app
from models import User, Mannschaft, Spiel

def clear_database():
    db.drop_all()
    db.create_all()

def initialize_admin_user():
    admin_user = User(
        id=1,
        email="admin@example.com",
        password=generate_password_hash("adminpassword123#+GT", method='pbkdf2:sha256'),
        name="Administrator",
        role="admin"
    )
    db.session.add(admin_user)
    db.session.commit()

def initialize_mannschaften():
    mannschaften = [
        {"abkuerzung": "ALB", "name": "Albanien", "em_titel": 0},
        {"abkuerzung": "BEL", "name": "Belgien", "em_titel": 0},
        {"abkuerzung": "DEN", "name": "Dänemark", "em_titel": 1},
        {"abkuerzung": "GER", "name": "Deutschland", "em_titel": 3},
        {"abkuerzung": "ENG", "name": "England", "em_titel": 0},
        {"abkuerzung": "FRA", "name": "Frankreich", "em_titel": 2},
        {"abkuerzung": "GEO", "name": "Georgien", "em_titel": 0},
        {"abkuerzung": "ITA", "name": "Italien", "em_titel": 2},
        {"abkuerzung": "CRO", "name": "Kroatien", "em_titel": 0},
        {"abkuerzung": "NED", "name": "Niederlande", "em_titel": 1},
        {"abkuerzung": "AUT", "name": "Österreich", "em_titel": 0},
        {"abkuerzung": "POL", "name": "Polen", "em_titel": 0},
        {"abkuerzung": "POR", "name": "Portugal", "em_titel": 1},
        {"abkuerzung": "ROU", "name": "Rumänien", "em_titel": 0},
        {"abkuerzung": "SCO", "name": "Schottland", "em_titel": 0},
        {"abkuerzung": "SUI", "name": "Schweiz", "em_titel": 0},
        {"abkuerzung": "SRB", "name": "Serbien", "em_titel": 0},
        {"abkuerzung": "SVK", "name": "Slowakei", "em_titel": 0},
        {"abkuerzung": "SVN", "name": "Slowenien", "em_titel": 0},
        {"abkuerzung": "ESP", "name": "Spanien", "em_titel": 3},
        {"abkuerzung": "CZE", "name": "Tschechien", "em_titel": 0},
        {"abkuerzung": "TUR", "name": "Türkei", "em_titel": 0},
        {"abkuerzung": "UKR", "name": "Ukraine", "em_titel": 0},
        {"abkuerzung": "HUN", "name": "Ungarn", "em_titel": 0},
        {"abkuerzung": "DUMMY_GAST", "name": "Dummy Gastmannschaft", "em_titel": 0},
        {"abkuerzung": "DUMMY_HEIM", "name": "Dummy Heimmannschaft", "em_titel": 0}
    ]

    for team in mannschaften:
        mannschaft = Mannschaft(
            abkuerzung=team["abkuerzung"],
            name=team["name"],
            logo=f"{team['abkuerzung']}.png",  # Setze das Logo basierend auf der Abkürzung
            em_titel=team["em_titel"]
        )
        db.session.add(mannschaft)

    db.session.commit()

def initialize_spiele():
    spiele = [
        # Gruppe A
        {"datum": "2024-06-14 21:00", "stadion": "Allianz Arena, München", "gast": "SCO", "heim": "GER",
         "typ": "Vorrunde", "gruppe": "A"},
        {"datum": "2024-06-15 15:00", "stadion": "Rheinenergiestadion, Köln", "gast": "SUI", "heim": "HUN",
         "typ": "Vorrunde", "gruppe": "A"},
        {"datum": "2024-06-19 21:00", "stadion": "Rheinenergiestadion, Köln", "gast": "SUI", "heim": "SCO",
         "typ": "Vorrunde", "gruppe": "A"},
        {"datum": "2024-06-19 18:00", "stadion": "Mercedes-Benz Arena, Stuttgart", "gast": "HUN", "heim": "GER",
         "typ": "Vorrunde", "gruppe": "A"},
        {"datum": "2024-06-23 21:00", "stadion": "Deutsche Bank Park, Frankfurt", "gast": "GER", "heim": "SUI",
         "typ": "Vorrunde", "gruppe": "A"},
        {"datum": "2024-06-23 21:00", "stadion": "Mercedes-Benz Arena, Stuttgart", "gast": "HUN", "heim": "SCO",
         "typ": "Vorrunde", "gruppe": "A"},
        # Gruppe B
        {"datum": "2024-06-15 18:00", "stadion": "Olympiastadion, Berlin", "gast": "CRO", "heim": "ESP",
         "typ": "Vorrunde", "gruppe": "B"},
        {"datum": "2024-06-15 21:00", "stadion": "Signal-Iduna-Park, Dortmund", "gast": "ALB", "heim": "ITA",
         "typ": "Vorrunde", "gruppe": "B"},
        {"datum": "2024-06-19 15:00", "stadion": "Volksparkstadion, Hamburg", "gast": "CRO", "heim": "ALB",
         "typ": "Vorrunde", "gruppe": "B"},
        {"datum": "2024-06-20 21:00", "stadion": "Veltins-Arena, Gelsenkirchen", "gast": "ITA", "heim": "ESP",
         "typ": "Vorrunde", "gruppe": "B"},
        {"datum": "2024-06-24 21:00", "stadion": "Merkur Spiel-Arena, Düsseldorf", "gast": "ESP", "heim": "ALB",
         "typ": "Vorrunde", "gruppe": "B"},
        {"datum": "2024-06-24 21:00", "stadion": "Red Bull Arena, Leipzig", "gast": "ITA", "heim": "CRO",
         "typ": "Vorrunde", "gruppe": "B"},
        # Gruppe C
        {"datum": "2024-06-16 18:00", "stadion": "Mercedes-Benz Arena, Stuttgart", "gast": "DEN", "heim": "SVN",
         "typ": "Vorrunde", "gruppe": "C"},
        {"datum": "2024-06-16 21:00", "stadion": "Veltins-Arena, Gelsenkirchen", "gast": "ENG", "heim": "SRB",
         "typ": "Vorrunde", "gruppe": "C"},
        {"datum": "2024-06-20 18:00", "stadion": "Deutsche Bank Park, Frankfurt", "gast": "ENG", "heim": "DEN",
         "typ": "Vorrunde", "gruppe": "C"},
        {"datum": "2024-06-20 15:00", "stadion": "Allianz Arena, München", "gast": "SRB", "heim": "SVN",
         "typ": "Vorrunde", "gruppe": "C"},
        {"datum": "2024-06-25 21:00", "stadion": "Rheinenergiestadion, Köln", "gast": "SVN", "heim": "ENG",
         "typ": "Vorrunde", "gruppe": "C"},
        {"datum": "2024-06-25 21:00", "stadion": "Allianz Arena, München", "gast": "SRB", "heim": "DEN",
         "typ": "Vorrunde", "gruppe": "C"},
        # Gruppe D
        {"datum": "2024-06-16 15:00", "stadion": "Volksparkstadion, Hamburg", "gast": "NED", "heim": "POL",
         "typ": "Vorrunde", "gruppe": "D"},
        {"datum": "2024-06-17 21:00", "stadion": "Merkur Spiel-Arena, Düsseldorf", "gast": "FRA", "heim": "AUT",
         "typ": "Vorrunde", "gruppe": "D"},
        {"datum": "2024-06-21 18:00", "stadion": "Olympiastadion, Berlin", "gast": "AUT", "heim": "POL",
         "typ": "Vorrunde", "gruppe": "D"},
        {"datum": "2024-06-21 21:00", "stadion": "Red Bull Arena, Leipzig", "gast": "FRA", "heim": "NED",
         "typ": "Vorrunde", "gruppe": "D"},
        {"datum": "2024-06-25 18:00", "stadion": "Signal-Iduna-Park, Dortmund", "gast": "POL", "heim": "FRA",
         "typ": "Vorrunde", "gruppe": "D"},
        {"datum": "2024-06-25 18:00", "stadion": "Olympiastadion, Berlin", "gast": "AUT", "heim": "NED",
         "typ": "Vorrunde", "gruppe": "D"},
        # Gruppe E
        {"datum": "2024-06-17 18:00", "stadion": "Deutsche Bank Park, Frankfurt", "gast": "SVK", "heim": "BEL",
         "typ": "Vorrunde", "gruppe": "E"},
        {"datum": "2024-06-17 15:00", "stadion": "Allianz Arena, München", "gast": "UKR", "heim": "ROU",
         "typ": "Vorrunde", "gruppe": "E"},
        {"datum": "2024-06-21 15:00", "stadion": "Merkur Spiel-Arena, Düsseldorf", "gast": "UKR", "heim": "SVK",
         "typ": "Vorrunde", "gruppe": "E"},
        {"datum": "2024-06-22 21:00", "stadion": "Rheinenergiestadion, Köln", "gast": "ROU", "heim": "BEL",
         "typ": "Vorrunde", "gruppe": "E"},
        {"datum": "2024-06-26 18:00", "stadion": "Mercedes-Benz Arena, Stuttgart", "gast": "BEL", "heim": "UKR",
         "typ": "Vorrunde", "gruppe": "E"},
        {"datum": "2024-06-26 18:00", "stadion": "Deutsche Bank Park, Frankfurt", "gast": "ROU", "heim": "SVK",
         "typ": "Vorrunde", "gruppe": "E"},
        # Gruppe F
        {"datum": "2024-06-18 18:00", "stadion": "Signal-Iduna-Park, Dortmund", "gast": "GEO", "heim": "TUR",
         "typ": "Vorrunde", "gruppe": "F"},
        {"datum": "2024-06-18 21:00", "stadion": "Red Bull Arena, Leipzig", "gast": "CZE", "heim": "POR",
         "typ": "Vorrunde", "gruppe": "F"},
        {"datum": "2024-06-22 18:00", "stadion": "Signal-Iduna-Park, Dortmund", "gast": "POR", "heim": "TUR",
         "typ": "Vorrunde", "gruppe": "F"},
        {"datum": "2024-06-22 15:00", "stadion": "Volksparkstadion, Hamburg", "gast": "CZE", "heim": "GEO",
         "typ": "Vorrunde", "gruppe": "F"},
        {"datum": "2024-06-26 21:00", "stadion": "Volksparkstadion, Hamburg", "gast": "TUR", "heim": "CZE",
         "typ": "Vorrunde", "gruppe": "F"},
        {"datum": "2024-06-26 21:00", "stadion": "Veltins-Arena, Gelsenkirchen", "gast": "POR", "heim": "GEO",
         "typ": "Vorrunde", "gruppe": "F"},
        # Achtelfinale
        {"datum": "2024-06-29 21:00", "stadion": "Signal-Iduna-Park, Dortmund", "gast": "DUMMY_GAST",
         "heim": "DUMMY_HEIM", "typ": "Achtelfinale 1", "gruppe": None, "locked": True},
        {"datum": "2024-06-29 18:00", "stadion": "Olympiastadion, Berlin", "gast": "DUMMY_GAST", "heim": "DUMMY_HEIM",
         "typ": "Achtelfinale 2", "gruppe": None, "locked": True},
        {"datum": "2024-06-30 21:00", "stadion": "Rheinenergiestadion, Köln", "gast": "DUMMY_GAST",
         "heim": "DUMMY_HEIM", "typ": "Achtelfinale 3", "gruppe": None, "locked": True},
        {"datum": "2024-06-30 18:00", "stadion": "Veltins-Arena, Gelsenkirchen", "gast": "DUMMY_GAST",
         "heim": "DUMMY_HEIM", "typ": "Achtelfinale 4", "gruppe": None, "locked": True},
        {"datum": "2024-07-01 21:00", "stadion": "Deutsche Bank Park, Frankfurt", "gast": "DUMMY_GAST",
         "heim": "DUMMY_HEIM", "typ": "Achtelfinale 5", "gruppe": None, "locked": True},
        {"datum": "2024-07-01 18:00", "stadion": "Merkur Spiel-Arena, Düsseldorf", "gast": "DUMMY_GAST",
         "heim": "DUMMY_HEIM", "typ": "Achtelfinale 6", "gruppe": None, "locked": True},
        {"datum": "2024-07-02 18:00", "stadion": "Allianz Arena, München", "gast": "DUMMY_GAST", "heim": "DUMMY_HEIM",
         "typ": "Achtelfinale 7", "gruppe": None, "locked": True},
        {"datum": "2024-07-02 21:00", "stadion": "Red Bull Arena, Leipzig", "gast": "DUMMY_GAST", "heim": "DUMMY_HEIM",
         "typ": "Achtelfinale 8", "gruppe": None, "locked": True},
        # Viertelfinale
        {"datum": "2024-07-05 18:00", "stadion": "Mercedes-Benz Arena, Stuttgart", "gast": "DUMMY_GAST",
         "heim": "DUMMY_HEIM", "typ": "Viertelfinale 1", "gruppe": None, "locked": True},
        {"datum": "2024-07-05 21:00", "stadion": "Volksparkstadion, Hamburg", "gast": "DUMMY_GAST",
         "heim": "DUMMY_HEIM", "typ": "Viertelfinale 2", "gruppe": None, "locked": True},
        {"datum": "2024-07-06 21:00", "stadion": "Olympiastadion, Berlin", "gast": "DUMMY_GAST", "heim": "DUMMY_HEIM",
         "typ": "Viertelfinale 3", "gruppe": None, "locked": True},
        {"datum": "2024-07-06 18:00", "stadion": "Merkur Spiel-Arena, Düsseldorf", "gast": "DUMMY_GAST",
         "heim": "DUMMY_HEIM", "typ": "Viertelfinale 4", "gruppe": None, "locked": True},
        # Halbfinale
        {"datum": "2024-07-09 21:00", "stadion": "Allianz Arena, München", "gast": "DUMMY_GAST", "heim": "DUMMY_HEIM",
         "typ": "Halbfinale 1", "gruppe": None, "locked": True},
        {"datum": "2024-07-10 21:00", "stadion": "Signal-Iduna-Park, Dortmund", "gast": "DUMMY_GAST",
         "heim": "DUMMY_HEIM", "typ": "Halbfinale 2", "gruppe": None, "locked": True},
        # Finale
        {"datum": "2024-07-14 21:00", "stadion": "Olympiastadion, Berlin", "gast": "DUMMY_GAST", "heim": "DUMMY_HEIM",
         "typ": "Finale", "gruppe": None, "locked": True},
    ]

    for spiel in spiele:
        gast_mannschaft = Mannschaft.query.filter_by(abkuerzung=spiel["gast"]).first()
        heim_mannschaft = Mannschaft.query.filter_by(abkuerzung=spiel["heim"]).first()
        datum = datetime.strptime(spiel["datum"], "%Y-%m-%d %H:%M")

        spiel_instance = Spiel(
            datum=datum,
            gast_mannschaft_id=gast_mannschaft.id if gast_mannschaft else None,
            heim_mannschaft_id=heim_mannschaft.id if heim_mannschaft else None,
            typ=spiel["typ"],
            tore_gast=spiel.get("tore_gast", 0),
            tore_heim=spiel.get("tore_heim", 0),
            austragungsort=spiel["stadion"],
            gruppe=spiel["gruppe"],
            absolviert=spiel.get("absolviert", False),
            locked=spiel.get("locked", False)
        )
        db.session.add(spiel_instance)

    db.session.commit()


with app.app_context():
    clear_database()
    db.create_all()
    initialize_admin_user()
    initialize_mannschaften()
    initialize_spiele()
    print("Alles erzeugt!")
