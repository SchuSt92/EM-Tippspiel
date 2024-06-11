from flask import Blueprint

# Blueprint für alle Seiten für die eine Authentifizierung notwendig ist.
auth = Blueprint('auth', __name__)


@auth.route('/register', methods=["GET"])
def register():
    return "Registrieren"


# Übermittelung der Formular Daten
#Regestrierung und Erstellung von den benötigten DB-Einträgen für einen Nutzer. (z.B. Tipps, Account etc.
# )
@auth.route('/register', methods=["POST"])
def register_post():
    return "Registrieren - POST"



@auth.route('/login', methods=["GET"])
def login():
    return "Login"


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
