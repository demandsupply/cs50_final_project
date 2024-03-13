import os
from flask import Flask, redirect, render_template, request, jsonify, session, flash
from cs50 import SQL
from flask_session import Session
import requests
import json
import param
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps

# USERS         giovaz      tom         kenny           bob
# PASSWORDS     giovaz12    tom12345    kenny123        bob12345

# Configure application
app = Flask(__name__)


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Configure sql database
db = SQL("sqlite:///finalproject.db")


headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI3Yjg3YzFlNzU4ZTNkNzA4YzUyMmUyYmUyN2FjYjBhMCIsInN1YiI6IjY1Y2U3MzM0YTMxNDQwMDE2MmE2ZGMwZCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.Azo3xqnhGWGHEv7B_Genf96HVFJcEBfJki1_vZBN0W0"
}


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        
        username = request.form.get("username")
        # Check if input is blank
        if (not username):
            flash("Insert a username")
            return redirect("/register")

        # Check if the chosen username is already used
        temporary = db.execute("SELECT username FROM users WHERE username = ? LIMIT 1", username)
        for dict in temporary:
            if dict["username"] == username:
                flash("Name already used")
                return redirect("/register")
    
        password = request.form.get("password")

        # Check if input is blank
        if (not password):
            flash("Insert a password")
            return redirect("/register")
        
        # Check if the password has at least: 1 letter, 1 number, lenght = 8
        if (len(password) != 8):
            flash("Password must have 8 characters")
            return redirect("/register")
        elif (password.isalpha() == True or password.isdigit() == True ):
            flash("Password must contain at least one character and one number")
            return redirect("/register")

        confirmation = request.form.get("confirm")

        # Check if password matches
        if (password != confirmation):
            flash("password is not the same!")
            return redirect("/register")
        # print(f"values are: {username, password, confirmation}")

        # Insert the new user into users and store a hash of its password
        hash = generate_password_hash(password)
        db.execute("INSERT INTO users(username, hash) VALUES(?, ?)", username, hash)

    return render_template("register.html")

@app.route("/layout", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            flash("Must provide username")
            return redirect("/")

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("Must provide password")
            return redirect("/")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        print(rows)

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            flash("invalid username and/or password")
            return redirect("/")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        # return redirect("/")
        return render_template("index.html", name=rows[0]["username"])


    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("index.html", name=rows[0]["username"])

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")   

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        movie = "inception"
        # movie = request.args.get("movie")
        print(movie)
        limit = 50
        page = 0
        response_list = []
        json_response_list = []
        while (page < limit):
            if page == 0:
                url = f"https://api.themoviedb.org/3/search/movie?query={movie}"
            else:
                url = f"https://api.themoviedb.org/3/search/movie?query={movie}&page={page+1}"

            print(url)
            response = requests.get(url, headers=headers)
            
            print(response)
            
            json_response = json.loads(response.text)
            # print(response.text)

            if not json_response["results"]:
                break

            print(f"THIS IS PAGE {page + 1}")
            print(json_response)

            page = page + 1
            response_list.append(response)
            json_response_list.append(json_response)
        # print(response_list)
        # print(json_response_list)

        return render_template("index.html", movie=movie, response=response_list, json_response=json_response_list)

    else:
        movie = request.form.get("movie")
        print(movie)
        return redirect("/")

@app.route("/movie/<id>", methods = ["GET", "POST"])
def movie_id(id):
    if request.method == ("POST"):
        username = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])
        print(id)
        favorite = db.execute("SELECT movie_title, username FROM favoritesmovies WHERE movie_id = ? AND username = ?", id, username[0]["username"]) 
        print(favorite)
        if favorite:
            print("movie exist, I'll remove it")
            db.execute("DELETE FROM favoritesmovies WHERE movie_id = ? AND username = ?", id, username[0]["username"]) 
            button = "add"
        else:
            print("movie does not exist, I'll add it")
            db.execute("INSERT INTO favoritesmovies (username, movie_title, movie_id) VALUES (?, 'gio', ?)", username[0]["username"], id) 
            button = "remove"
    else:
        username = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])
        print(id)
        favorite = db.execute("SELECT movie_title, username FROM favoritesmovies WHERE movie_id = ? AND username = ?", id, username[0]["username"]) 
        print(favorite)
        if favorite:
            print("movie exist")
            button = "remove"
        else:
            print("movie does not exist")
            button = "add"

    
    print(f"id is {id}")

    url = f"https://api.themoviedb.org/3/movie/{id}"
    print(url)
    response = requests.get(url, headers=headers)
    print(response)
    
    if response.status_code == 200:
        movie_datas = json.loads(response.text)
        # print(movie_datas)
    return render_template ("movie.html", movie_datas=movie_datas, button=button)



@app.route("/ajax", methods=["GET", "POST"])
def ajax():
    if request.method == "GET":
        return render_template("ajax.html")
    else:
        q = request.form.get("q")
        if q:
            url = f"https://api.themoviedb.org/3/search/movie?query={q}&page=1"

            print(url)
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                shows = json.loads(response.text)
                print(shows)
                return jsonify(shows)
    return jsonify({"error": "Invalid request"})

@app.route("/data", methods=["GET", "POST"])
def data():
    if request.method == "GET":
        favorites_list = []
        users = db.execute("SElECT * FROM users")
        favorites = db.execute("SElECT * FROM favoritesmovies")
        print(f"favorites are {favorites}")
        for movie in favorites:
            q = movie["movie_id"]
            # print(q)
            url = f"https://api.themoviedb.org/3/movie/{q}"
            response = requests.get(url, headers=headers)
            movie_data = json.loads(response.text)
            favorites_list.append(movie_data)
            print(movie_data["title"])

        zip_list = zip(favorites, favorites_list)    
        return render_template ("data.html", users=users, favorites=favorites, favorites_list=favorites_list, zip_list=zip_list)
    
    else:
        remove_id = request.form.get("id")
        db.execute("DELETE FROM users WHERE id = ?", remove_id)
        return redirect ("/data")