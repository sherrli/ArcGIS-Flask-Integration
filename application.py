from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/smalltrails")
def smalltrails():
    return render_template("smalltrails.html")

@app.route("/diseases")
def diseases():
    return render_template("diseases.html")
