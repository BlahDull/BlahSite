from flask import Flask, render_template

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

@app.route("/login.html")
def login_page():
    return render_template("login.html")