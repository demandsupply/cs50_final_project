import os
from flask import Flask, redirect, render_template, request, jsonify, session, flash, url_for
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

@app.route("/login", methods=["GET", "POST"])
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
        session["user"] = rows[0]["username"]

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
        return render_template("index.html")

    else:
        selected = request.form.get("media")
        print(selected)

        title = request.form.get("title")
        print(title)

        limit = 50
        page = 0
        response_list = []
        json_response_list = []


        if selected == "movie":
            print("movie selected")
        
            while (page < limit):
                
                if page == 0:
                    url = f"https://api.themoviedb.org/3/search/movie?query={title}"
                else:
                    url = f"https://api.themoviedb.org/3/search/movie?query={title}&page={page+1}"

                print(url)
                response = requests.get(url, headers=headers)
                
                print(response)
                
                json_response = json.loads(response.text)
                # print(response.text)

                if not json_response["results"]:
                    break

                # print(f"THIS IS PAGE {page + 1}")
                # print(json_response)

                page = page + 1
                response_list.append(response)
                json_response_list.append(json_response)
            # print(response_list)
            # print(json_response_list)
            return render_template("index.html", title=title, response=response_list, json_response=json_response_list, externlink="movie", internlink="movie")
                
                
        elif selected == "tv-show":
            print("tv-show selected")
        
            while (page < limit):
                
                if page == 0:
                    url = f"https://api.themoviedb.org/3/search/tv?query={title}"
                else:
                    url = f"https://api.themoviedb.org/3/search/tv?query={title}&page={page+1}"

                print(url)
                response = requests.get(url, headers=headers)
                
                print(response)
                
                json_response = json.loads(response.text)
                # print(response.text)

                if not json_response["results"]:
                    break

                # print(f"THIS IS PAGE {page + 1}")
                # print(json_response)

                page = page + 1
                response_list.append(response)
                json_response_list.append(json_response)
            print(response_list)
            print(json_response_list)
            return render_template("index.html", title=title, response=response_list, json_response=json_response_list, externlink="tv", internlink="tvshow")
                
                


@app.route("/movie/<id>", methods = ["GET", "POST"])
def movie_id(id):
    
    print(f"id is {id}")

    url = f"https://api.themoviedb.org/3/movie/{id}"
    print(url)
    response = requests.get(url, headers=headers)
    print(response)
    if response.status_code == 200:
        movie_datas = json.loads(response.text)
        # print(movie_datas)

    if request.method == ("GET"):
        print("request method is get")
        username = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])
        favorite = db.execute("SELECT movie_title, username FROM usersmovies WHERE movie_id = ? AND category = 'favorite' AND username = ?", id, username[0]["username"]) 
        watchlist = db.execute("SELECT movie_title, username FROM usersmovies WHERE movie_id = ? AND category = 'watchlist' AND username = ?", id, username[0]["username"]) 
        # print(favorite)
        # print(watchlist)
        if favorite:
            print("movie exist")
            button_favorites = "remove from favorites"
        else:
            print("movie does not exist")
            button_favorites = "add to favorites"

        if watchlist:
            print("movie exist")
            button_watchlist = "remove from watchlist"
        else:
            print("movie does not exist")
            button_watchlist = "add to watchlist"

        return render_template ("movie.html", movie_datas=movie_datas, button_favorites=button_favorites, button_watchlist=button_watchlist)


    else:
        print("request method is post")
        # if (request.form.get("favorite")):
        username = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])
        favorite = db.execute("SELECT movie_title, username FROM usersmovies WHERE movie_id = ?  AND category = 'favorite' AND username = ?", id, username[0]["username"]) 
        watchlist = db.execute("SELECT movie_title, username FROM usersmovies WHERE movie_id = ? AND category = 'watchlist' AND username = ?", id, username[0]["username"]) 

        button_favorites = "remove from favorites"
        button_watchlist = "remove from watchlist"

        if not favorite:
            button_favorites = "add to favorites"
        if not watchlist:
            button_watchlist = "add to watchlist"

        if request.form.get('favorite') == 'remove from favorites':
            print("favorite")
            print("movie exist of favorite, I'll remove it")
            db.execute("DELETE FROM usersmovies WHERE movie_id = ? AND category = 'favorite' AND username = ?", id, username[0]["username"]) 
            button_favorites = "add to favorites"
        if request.form.get('favorite') == 'add to favorites':
            print("movie does not exist on favorite, I'll add it")
            db.execute("INSERT INTO usersmovies (username, movie_title, movie_id, category) VALUES (?, 'gio', ?, 'favorite')", username[0]["username"], id) 
            button_favorites = "remove from favorites"
                

        if request.form.get('watchlist') == 'remove from watchlist':
            print("movie exist on watchlist, I'll remove it")
            db.execute("DELETE FROM usersmovies WHERE movie_id = ? AND category = 'watchlist' AND username = ?", id, username[0]["username"]) 
            button_watchlist = "add to watchlist"

        if request.form.get('watchlist') == 'add to watchlist':
            print("movie does not exist on watchlist, I'll add it")
            db.execute("INSERT INTO usersmovies (username, movie_title, movie_id, category) VALUES (?, 'gio', ?, 'watchlist')", username[0]["username"], id) 
            button_watchlist = "remove from watchlist"
                        
        else:
            print("no button clicked")


        return redirect(url_for("movie_id", id=id))

60059 - 60223
@app.route("/tvshow/<id>", methods = ["GET", "POST"])
def tvshow_id(id):
    
    print(f"id is {id}")

    url = f"https://api.themoviedb.org/3/tv/{id}"
    print(url)
    response = requests.get(url, headers=headers)
    print(response.text)
    if response.status_code == 200:
        show_datas = json.loads(response.text)
        # print(movie_datas)

    print(show_datas)
    number_of_seasons = show_datas["number_of_seasons"]
    print(f"aaaaaaaaaaaaa is {number_of_seasons}")
    if request.method == ("GET"):
        print("request method is get")
        # print(response.text)
        username = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])
        episodes_data = []
        sort = " | sort(attribute = 'vote_average', reverse=true)"
        for season in range(number_of_seasons + 1):
            if season == 0:
                continue
            else:
                season_data_url = f"https://api.themoviedb.org/3/tv/{id}/season/{season}"
                response_season_data = requests.get(season_data_url, headers=headers)
                season_data = json.loads(response_season_data.text)
                print(season_data["name"])            

                for episode in season_data["episodes"]:
                    episodes_data.append(episode)
                    # print(f"episode number {episode_number}")
                # print(season_data["episodes"][0]["episode_number"])
                # print(season_data["episodes"][0]["overview"])
        


        for episode in episodes_data:
            print(episode["season_number"])
            print(episode["episode_number"])
            # print(episode)
        print(number_of_seasons)
        return render_template ("tvshow.html", number_of_seasons=number_of_seasons, movie_datas=show_datas, episodes_data=episodes_data)


    else:
        print("request method is post")
        return redirect(url_for("tvshow_id", id=id))

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

@app.route("/toprated", methods=["GET"])
def top_rated():
    if request.method == "GET":
        pages = 6
        response_list = []
        for page in range(pages):
            url = f"https://api.themoviedb.org/3/movie/top_rated?language=en-US&page={page}"

            response = requests.get(url, headers=headers)
            movie_data = json.loads(response.text)
            response_list.append(movie_data)
        print(response_list)

        return render_template("toprated.html", response_list=response_list)

@app.route("/data", methods=["GET", "POST"])
def data():
    if request.method == "GET":
        favorites_list = []
        users = db.execute("SElECT * FROM users")
        favorites = db.execute("SElECT * FROM usersmovies")
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