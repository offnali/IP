from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import mysql.connector

views = Blueprint('views', __name__)


#--------------------------- DATABASE ---------------------------#
host="127.0.0.1"
user="nali"
password="nali"
database="ip1"

def create_connection(user, password, host, database):
    conn = mysql.connector.connect(user=user, password=password, host=host, database=database)
    return conn

conn = create_connection(user, password, host, database)
#--------------------------- DATABASE ---------------------------#


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

        if not username or not password:
            flash('Please fill in both username and password fields', 'error')
            return redirect(url_for('views.login'))
        
        cursor = conn.cursor()
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        values = (username, password)
        cursor.execute(query, values)
        result = cursor.fetchone()
        cursor.close()

        if not result:
            flash('Incorrect username or password', 'error')
            return redirect(url_for("views.login"))
        
        session['username-logpage'] = username
        return redirect(url_for("views.home"))
    return render_template("login.html")
#--------------------------- LOGIN ---------------------------#


#--------------------------- REGISTER ---------------------------#
@views.route('/sign-up', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if not username or not password or not confirm_password:
            flash("All fields are required", "error")
            return redirect(url_for("views.register"))

        if password != confirm_password:
            flash("Passwords do not match. Please try again.", "error")
            return redirect(url_for("views.register"))

        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

        if user:
            flash("username already exists. Please try again.", "error")
            return redirect(url_for("views.register"))

        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        conn.commit()
        cursor.close()

        flash("Registration successful. Thank you for registering!", "success")
        return redirect(url_for("views.register"))
    
    return render_template('register.html')
#--------------------------- REGISTER ---------------------------#


#--------------------------- Log Out ---------------------------#
@views.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('views.home'))
#--------------------------- Log Out ---------------------------#