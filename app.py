import os
from flask import Flask, redirect, render_template, request
from cs50 import SQL

# Configure application
app = Flask(__name__)



@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")