from flask import Flask, render_template, request, jsonify
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def home_page():
    return render_template("index.html")

@app.route("/about.html")
def about_page():
    return render_template("about.html")

@app.route("/chat.html")
def chat_page():
    return render_template("chat.html")

@app.route("/chat.html", methods=['POST'])
def save_message():
    msg = request.form['message']
    with open("messages.txt", "a") as file:
        file.write(f"{datetime.now()}: {msg}\n")
    return jsonify({'message': 'Message received'})

@app.route("/login.html")
def login_page():
    return render_template("login.html")