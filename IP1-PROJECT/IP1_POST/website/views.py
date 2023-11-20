from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import mysql.connector, re
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from flask_bcrypt import Bcrypt

views = Blueprint('views', __name__)

# Initialisatie van de bcrypt.
bcrypt = Bcrypt()


#--------------------------- DATABASE ---------------------------#
# Om connectie maken met de database.
host="127.0.0.1"
user="nali"
password="nali"
database="ip1post"

def create_connection(user, password, host, database):
    conn = mysql.connector.connect(user=user, password=password, host=host, database=database)
    return conn

conn = create_connection(user, password, host, database)
#--------------------------- DATABASE ---------------------------#


#--------------------------- DATABASE CLEAN-UP ---------------------------#
# Oude IP's opschonen van de database.
scheduler = BackgroundScheduler()
scheduler.start()

def remove_expired_attempts():
    expiration_time = datetime.now() - timedelta(minutes=5)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM login_attempts WHERE last_attempt < %s", (expiration_time,))
    conn.commit()
    cursor.close()

# Een taak inplannen dat elk 30 minuten wordt uitgevoerd
scheduler.add_job(remove_expired_attempts, 'interval', minutes=30)
#--------------------------- DATABASE CLEAN-UP ---------------------------#


#--------------------------- CHECK BLOCK STATUS ---------------------------#
# een functie dat controleert op een bepaald IP geblokkeerd is.
def check_block_status(ip_address):
    cursor = conn.cursor()
    cursor.execute("SELECT attempts, last_attempt FROM login_attempts WHERE ip_address = %s", (ip_address,))
    login_attempts = cursor.fetchone()

    if login_attempts and login_attempts[0] >= 10:
        last_attempt_time = login_attempts[1]
        block_duration = timedelta(minutes=5)
        elapsed_time = datetime.now() - last_attempt_time

        if elapsed_time < block_duration:
            remaining_time = block_duration - elapsed_time
            flash(f'Too many login attempts. You are blocked for {remaining_time}.', 'error')
            return True  # Teruggeven dat de inlogpogingen zijn geblokkeerd

    return False  # Teruggeven dat de inlogpogingen niet zijn geblokkeerd
#--------------------------- CHECK BLOCK STATUS ---------------------------#


#--------------------------- LOGIN ATTEMPTS UPDATE ---------------------------#
# een functie dat de inlogpoging in de database update na een foutief inlogpoging.
def update_login_attempts(ip_address):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM login_attempts WHERE ip_address = %s", (ip_address,))
    record = cursor.fetchone()

    if record:
        cursor.execute("UPDATE login_attempts SET attempts = attempts + 1 WHERE ip_address = %s", (ip_address,))
    else:
        cursor.execute("INSERT INTO login_attempts (ip_address, attempts) VALUES (%s, 1)", (ip_address,))

    conn.commit()
    cursor.close()
#--------------------------- LOGIN ATTEMPTS UPDATE ---------------------------#


#--------------------------- PASSWORD STRENGTH POLICY ---------------------------#
def is_password_strong(password):
    # Functie voor Wachtwoord Beleid: Minimaal 8 karakters, 1 nummer, 1 kleine letter, 1 hoofdletter, 1 speciale symbool
    if (len(password) < 8 or
            not re.search(r"\d", password) or
            not re.search(r"[a-z]", password) or
            not re.search(r"[A-Z]", password) or
            not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)):
        return False
    return True
#--------------------------- PASSWORD STRENGTH POLICY ---------------------------#


#--------------------------- HOME ---------------------------#
@views.route('/')
def home():
    return render_template("base.html")
#--------------------------- HOME ---------------------------#


#--------------------------- LOGIN ---------------------------#
@views.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Ophalen van IP adress van de gebruiker.
        ip_address = request.remote_addr

        # Controleren of de gebruiker geblokt is
        if check_block_status(ip_address):
                return redirect(url_for('views.login'))

        # Controle of de invoervelden zijn ingevuld.
        if not username or not password:
            flash('Please fill in both username and password fields', 'error')
            return redirect(url_for('views.login'))
        
        # Verificatie van inloggegevens.
        cursor = conn.cursor()
        query = "SELECT password FROM users WHERE username = %s"
        values = (username,)
        cursor.execute(query, values)
        result = cursor.fetchone()

        # Verifiëren of de hash klopt.
        if not result or not bcrypt.check_password_hash(result[0], password):
            update_login_attempts(ip_address)

            flash('Incorrect username or password', 'error')
            return redirect(url_for("views.login"))

        # Gebruiker wordt uit de login_attempts lijst gehaald omdat de gebruiker successvol is ingelogd.
        cursor.execute("DELETE FROM login_attempts WHERE ip_address = %s", (ip_address,))
        conn.commit()
        cursor.close()

        # Sessie wordt aangemaakt.
        session['username-logpage'] = username
        return redirect(url_for("views.home"))
    
    # Ophalen van IP adress van de gebruiker.
    ip_address = request.remote_addr

    # Controleren of de gebruiker geblokt is.
    if check_block_status(ip_address):
            return render_template("login.html")

    return render_template("login.html")
#--------------------------- LOGIN ---------------------------#


#--------------------------- REGISTER ---------------------------#
@views.route('/sign-up', methods=['GET', 'POST'])
def register():
    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        # Validatie van data
        if not username or not password or not confirm_password:
            flash("All fields are required", "error")
            return redirect(url_for("views.register"))

        # Controle of de wachtwoorden matchen.
        if password != confirm_password:
            flash("Passwords do not match. Please try again.", "error")
            return redirect(url_for("views.register"))
        
        if not is_password_strong(password):
            flash("Password not strong enough. Please follow the password policy.", "error")
            return redirect(url_for("views.register"))

        # Check if username already exists
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

        if user:
            flash("username already exists. Please try again.", "error")
            return redirect(url_for("views.register"))
        # Het wachtwoord wordt gehasht met Bcrypt.
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Gebruiker toevoegen aan de database.
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
        conn.commit()
        cursor.close()

        flash("Registration successful. Thank you for registering!", "success")
        return redirect(url_for("views.register"))
    
    return render_template('register.html')
#--------------------------- REGISTER ---------------------------#


#--------------------------- Log Out ---------------------------#
@views.route('/logout')
def logout():
    # Sessie wordt Verwijderd.
    session.clear()
    return redirect(url_for('views.home'))
#--------------------------- Log Out ---------------------------#