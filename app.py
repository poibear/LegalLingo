import os
import math
from datetime import datetime
from flask import Flask, redirect, render_template, request, url_for, flash

app = Flask(__name__, template_folder="templates")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/form")
def form():     
    return render_template("survey.html")


if __name__ == "__main__":
    host = "127.0.0.1"
    port = "8080"
    app.config["TEMPLATES_AUTO_RELOAD"] = True # reload on html change
    app.secret_key = 'supa secretz'
    app.debug = True
    
    app.run(host=host, port=port)