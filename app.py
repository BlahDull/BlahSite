from flask import Flask, render_template, request, jsonify, url_for, redirect, session
from datetime import datetime
import sqlite3
import bcrypt
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = "placeholder_for_now"

@app.route("/")
def home_page():
    if 'logged_in' in session:
        return render_template("index.html", username=session['username'], logged_in=True)
    else:
        return render_template("index.html", username="Guest", logged_in=False)

@app.route("/about.html")
def about_page():
    return render_template("about.html")

@app.route("/chat.html")
def chat_page():
    if 'logged_in' in session:
        return render_template("chat.html")
    else:
        return redirect(url_for("login_page"))

@app.route("/chat.html", methods=['POST'])
def save_message():
    msg = request.form['message']
    with open("messages.txt", "a") as file:
        file.write(f"{datetime.now()}: {session['username']}: {msg}\n")
    return jsonify({'message': 'Message received'})

@app.route("/login.html")
def login_page():
    return render_template("login.html")

@app.route("/logout")
def logout_user():
    session.pop('username', None)
    session.pop('logged_in', None)
    return redirect(url_for("home_page"))

@app.route("/login.html", methods=['POST'])
def handle_login():
    action = request.form['action']
    if action == "signup":
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        if create_user(username, email, password):
            print("New User Created")
        else:
            print("Invalid Info")
            return jsonify({"result": "INVALID_CREDS"})
    elif action == "login":
        if login_user(request.form['email'], request.form['password']):
            print("Valid Creds")
        else:
            print("Wrong Creds")
            return jsonify({"result": "INVALID_CREDS"})
    return redirect(url_for("home_page"))

def valid_cred(password: str, email: str, username: str) -> bool:
    if (any(char.isdigit() for char in password)) == False:
        return False
    if (8 > len(password) or len(password) > 20):
        return False
    if re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email) == False:
        return False
    if (len(username) < 3 or len(username) > 20):
        return False
    return True
    
def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_pw = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed_pw

def create_user(username: str, email: str, password: str) -> bool:
    if (valid_cred(password, email, username)):
        password = hash_password(password)
        with sqlite3.connect("users.db") as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Users (email, password, username) VALUES (?, ?, ?)", (email, password, username))
            conn.commit()
        session['username'] = username
        session['logged_in'] = True
        return True
    else:
        return False
    
def login_user(email: str, password: str) -> bool:
    with sqlite3.connect("users.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Users WHERE email = ?", (email,))
        info = cursor.fetchone()
        if info:
            if validate_password(password, info[1]):
                session['username'] = info[2]
                session['logged_in'] = True
                return True
    return False

def validate_password(password: str, hashed_pw) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed_pw)