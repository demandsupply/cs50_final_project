import os
from flask import Flask, redirect, render_template, request, jsonify, session, flash, url_for
from cs50 import SQL
from flask_session import Session
import requests
import json
import param
import random
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
import ast


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
        return render_template("search.html", name=rows[0]["username"])


    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("search.html", name=rows[0]["username"])



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
        popular_movie_list = []
        popular_show_list = []

        movie_url = f"https://api.themoviedb.org/3/movie/popular"
        show_url = f"https://api.themoviedb.org/3/tv/popular"


        response = requests.get(movie_url, headers=headers)
        movie_data = json.loads(response.text)
        popular_movie_list.append(movie_data)
        print(popular_movie_list)

        response_show = requests.get(show_url, headers=headers)
        show_data = json.loads(response_show.text)
        popular_show_list.append(show_data)
        print(popular_show_list)

        while True:
            random_movie_id = random.randint(1, 1200000)
            url_random_movie = f"https://api.themoviedb.org/3/movie/{random_movie_id}"
            response_random_movie = requests.get(url_random_movie, headers=headers)
            if response_random_movie:
                random_movie_data = json.loads(response_random_movie.text)
                if random_movie_data["adult"] != True:
                    break
                else:
                    print(f"Adult content, load another movie")
            else:
                print(f"Movie does not exist, load another ID")
            
        return render_template("index.html", popular_movie_list=popular_movie_list, popular_show_list=popular_show_list, random_movie=random_movie_data)
    else:
        q = request.form.get("q")
        if q:
            url = f"https://api.themoviedb.org/3/search/multi?query={q}&page=1"

            print(url)
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                shows = json.loads(response.text)
                print(shows)
                return jsonify(shows)


@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "GET":
        return render_template("search.html")

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
            return render_template("search.html", title=title, response=response_list, json_response=json_response_list, externlink="movie", internlink="movie")
                
                
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
            return render_template("search.html", title=title, response=response_list, json_response=json_response_list, externlink="tv", internlink="tvshow")
                
                


@app.route("/movie/<id>", methods = ["GET", "POST"])
def item_id(id):
    
    print(f"id is {id}")

    url = f"https://api.themoviedb.org/3/movie/{id}"
    print(url)
    response = requests.get(url, headers=headers)
    print(response)
    if response.status_code == 200:
        movie_datas = json.loads(response.text)
        print(movie_datas)

    if request.method == ("GET"):
        print("request method is get")
        username = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])
        favorite = db.execute("SELECT title, username FROM favoriteswatchlist WHERE type = 'movie' AND item_id = ? AND category = 'favorite' AND username = ?", id, username[0]["username"]) 
        watchlist = db.execute("SELECT title, username FROM favoriteswatchlist WHERE type = 'movie' AND item_id = ? AND category = 'watchlist' AND username = ?", id, username[0]["username"]) 
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
        favorite = db.execute("SELECT title, username FROM favoriteswatchlist WHERE type = 'movie' AND item_id = ?  AND category = 'favorite' AND username = ?", id, username[0]["username"]) 
        watchlist = db.execute("SELECT title, username FROM favoriteswatchlist WHERE type = 'movie' AND item_id = ? AND category = 'watchlist' AND username = ?", id, username[0]["username"]) 

        button_favorites = "remove from favorites"
        button_watchlist = "remove from watchlist"

        if not favorite:
            button_favorites = "add to favorites"
        if not watchlist:
            button_watchlist = "add to watchlist"

        if request.form.get('favorite') == 'remove from favorites':
            print("favorite")
            print("movie exist of favorite, I'll remove it")
            db.execute("DELETE FROM favoriteswatchlist WHERE type = 'movie' AND item_id = ? AND category = 'favorite' AND username = ?", id, username[0]["username"]) 
            button_favorites = "add to favorites"
        if request.form.get('favorite') == 'add to favorites':
            print("movie does not exist on favorite, I'll add it")
            db.execute("INSERT INTO favoriteswatchlist (username, type, title, item_id, category) VALUES (?, 'movie', 'gio', ?, 'favorite')", username[0]["username"], id) 
            button_favorites = "remove from favorites"
                

        if request.form.get('watchlist') == 'remove from watchlist':
            print("movie exist on watchlist, I'll remove it")
            db.execute("DELETE FROM favoriteswatchlist WHERE type = 'movie' AND item_id = ? AND category = 'watchlist' AND username = ?", id, username[0]["username"]) 
            button_watchlist = "add to watchlist"

        if request.form.get('watchlist') == 'add to watchlist':
            print("movie does not exist on watchlist, I'll add it")
            db.execute("INSERT INTO favoriteswatchlist (username, type, title, item_id, category) VALUES (?, 'movie', 'gio', ?, 'watchlist')", username[0]["username"], id) 
            button_watchlist = "remove from watchlist"
                        
        else:
            print("no button clicked")


        return redirect(url_for("item_id", id=id))


@app.route("/tvshow/<id>", methods = ["GET", "POST"])
def tvshow_id(id):
    print(f"id is {id}")

    compare = []
    seasons_episodes_average_vote = []
    button_favorite_episodes = []
    url = f"https://api.themoviedb.org/3/tv/{id}"
    response = requests.get(url, headers=headers)
    print(response.text)
    if response.status_code == 200:
        show_datas = json.loads(response.text)
        # print(movie_datas)

    show_title = show_datas["name"]
    # print(f"THIS IS SHOW DATAS {show_datas['name']}")
    number_of_seasons = show_datas["number_of_seasons"]
    print(f"There are {number_of_seasons} seasons")

    username = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])

    episodes_data = []
    sort = " | sort(attribute = 'vote_average', reverse=true)"

    counter = 0

    for season in range(number_of_seasons + 1):
        if season == 0:
            continue
        else:
            url_season_data = f"https://api.themoviedb.org/3/tv/{id}/season/{season}"
            response_season_data = requests.get(url_season_data, headers=headers)
            season_data = json.loads(response_season_data.text)
            print(season_data["name"])     
            episode_average_vote = []


            for episode in season_data["episodes"]:
                counter = counter + 1
                episodes_data.append(episode)
                episode_average_vote.append(episode['vote_average'])

            # print(season_data["episodes"][0]["episode_number"])
            print(episode_average_vote)  
        seasons_episodes_average_vote.append(episode_average_vote)                      
        print(episode_average_vote)
    session["ratings"] = seasons_episodes_average_vote
    session["numberEpisodes"] = counter
    print(f"THEREARE {counter} EPISODES")
    for episode in episodes_data:
        print(f"season: {episode['season_number']}, ", end="")
        print(f"episode: {episode['episode_number']}, ", end="")
        print(f"vote average: {episode['vote_average']}")
        # print(episode)

    if request.method == ("GET"):
        print("request method is get")
        favorite = db.execute("SELECT title, username FROM favoriteswatchlist WHERE type = 'tv-show' AND item_id = ? AND category = 'favorite' AND username = ?", id, username[0]["username"]) 
        watchlist = db.execute("SELECT title, username FROM favoriteswatchlist WHERE type = 'tv-show' AND item_id = ? AND category = 'watchlist' AND username = ?", id, username[0]["username"]) 

        if favorite:
            print("tv-show exist")
            button_favorites = "remove from favorites"
        else:
            print("tv-show does not exist")
            button_favorites = "add to favorites"

        if watchlist:
            print("tv-show exist")
            button_watchlist = "remove from watchlist"
        else:
            print("tv-show does not exist")
            button_watchlist = "add to watchlist"


        episodes_data = []
        sort = " | sort(attribute = 'vote_average', reverse=true)"

        counter = 0

        for season in range(number_of_seasons + 1):
            if season == 0:
                continue
            else:
                url_season_data = f"https://api.themoviedb.org/3/tv/{id}/season/{season}"
                response_season_data = requests.get(url_season_data, headers=headers)
                season_data = json.loads(response_season_data.text)
                print(season_data["name"])     


                for episode in season_data["episodes"]:
                    counter = counter + 1
                    episodes_data.append(episode)
                    favorite_episodes = db.execute("SELECT episode_title, username FROM usershows WHERE episode_id = ? AND username = ?", episode["id"], username[0]["username"]) 

                    if favorite_episodes:
                        print("episode exist")
                        button_favorite_episodes.append("remove from favorite episodes")
                    else:
                        print("episode does not exist")
                        button_favorite_episodes.append("add to favorite episodes")
                    # print(f"episode number {episode_number}")
                # print(season_data["episodes"][0]["episode_number"])
            

        return render_template ("tvshow.html", button_favorite_episodes=button_favorite_episodes, button_favorites=button_favorites, button_watchlist=button_watchlist, number_of_seasons=number_of_seasons, show_datas=show_datas, episodes_data=episodes_data)

    else:
        print("request method is post")
        favorite = db.execute("SELECT title, username FROM favoriteswatchlist WHERE type = 'tv-show' AND item_id = ?  AND category = 'favorite' AND username = ?", id, username[0]["username"]) 
        watchlist = db.execute("SELECT title, username FROM favoriteswatchlist WHERE type = 'tv-show' AND item_id = ? AND category = 'watchlist' AND username = ?", id, username[0]["username"]) 
        compare = db.execute("SELECT show_title, username FROM compareshows WHERE show_title = ? AND username = ?", show_title, username[0]["username"]) 
        
        favorite_episodes = db.execute("SELECT episode_title, username FROM usershows WHERE show_id = ? AND username = ?", id, username[0]["username"]) 

        button_favorites = "remove from favorites"
        button_watchlist = "remove from watchlist"

        button_favorite_episodes = "remove from favorite_episodes"

        if not favorite:
            button_favorites = "add to favorites"
        if not watchlist:
            button_watchlist = "add to watchlist"

        if not favorite_episodes:
            button_favorite_episodes = "add to favorite episodes"

        if request.form.get('favorite') == 'remove from favorites':
            print("favorite")
            print("tv-show exist of favorite, I'll remove it")
            db.execute("DELETE FROM favoriteswatchlist WHERE type = 'tv-show' AND item_id = ? AND category = 'favorite' AND username = ?", id, username[0]["username"]) 
            button_favorites = "add to favorites"
        if request.form.get('favorite') == 'add to favorites':
            print("tv-show does not exist on favorite, I'll add it")
            db.execute("INSERT INTO favoriteswatchlist (username, type, title, item_id, category) VALUES (?, 'tv-show', 'gio', ?, 'favorite')", username[0]["username"], id) 
            button_favorites = "remove from favorites"
                

        if request.form.get('watchlist') == 'remove from watchlist':
            print("tv-show exist on watchlist, I'll remove it")
            db.execute("DELETE FROM favoriteswatchlist WHERE type = 'tv-show' AND item_id = ? AND category = 'watchlist' AND username = ?", id, username[0]["username"]) 
            button_watchlist = "add to watchlist"
        if request.form.get('watchlist') == 'add to watchlist':
            print("tv-show does not exist on watchlist, I'll add it")
            db.execute("INSERT INTO favoriteswatchlist (username, type, title, item_id, category) VALUES (?, 'tv-show', 'gio', ?, 'watchlist')", username[0]["username"], id) 
            button_watchlist = "remove from watchlist"
                        
        if request.form.get('favorite_episodes'): 
            episode_to_db_string = request.form.get('favorite_episodes') 
            print(f"EPISODE STRING DATAS ARE: {episode_to_db_string}")
            episode_to_db = ast.literal_eval(episode_to_db_string) 
            print(f"IIIIIIIDDDDDD IS ONE {episode_to_db['id']}")

            check_episode_on_db_list = db.execute("SELECT episode_id FROM usershows where episode_id = ?", episode_to_db["id"])

            if check_episode_on_db_list:
                print("episode saved on favorite episodes, I'll remove it")
                check_episode_on_db = check_episode_on_db_list[0]['episode_id']
                db.execute("DELETE FROM usershows WHERE episode_id = ?", check_episode_on_db)
                button_favorite_episodes = "add to favorites"
            else:
                print("episode is not saved on favorite episodes, I'll add it")
                db.execute("INSERT INTO usershows (username, show_title, show_id, season_number, episode_number, episode_title, episode_id) VALUES (?, ?, ?, ?, ?, ?, ?)", username[0]["username"], show_title, id, episode_to_db["season_number"], episode_to_db["episode_number"], episode_to_db["name"], episode_to_db["id"]) 
                button_favorite_episodes = "remove from favorites"
        
        if request.form.get('compare'):
            if not compare:
                list_to_string = ''.join(str(x) for x in seasons_episodes_average_vote)
                db.execute("INSERT INTO compareshows (username, show_title, episodes_ratings) VALUES (?, ?, ?)", username[0]["username"], show_title, list_to_string)
            return redirect(url_for("ajaxshows"))
        else:
            print("no button clicked")

        return redirect(url_for("tvshow_id", id=id))


@app.route("/tvshow/tv/<id>/season/<season>/episode/<seasonEpisode>", methods = ["GET", "POST"])
def episode(id, season, seasonEpisode):
    print(f"id {id}, season{season}, seasonEpisode{seasonEpisode}")

    username = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])       

    url = f"https://api.themoviedb.org/3/tv/{id}"
    response = requests.get(url, headers=headers)
    print(response.text)
    if response.status_code == 200:
        show_datas = json.loads(response.text)
        # print(movie_datas)

    show_title = show_datas["name"]
    # print(f"THIS IS SHOW DATAS {show_datas['name']}")
    number_of_seasons = show_datas["number_of_seasons"]
    print(f"There are {number_of_seasons} seasons")     
    
    url_episode_data = f"https://api.themoviedb.org/3/tv/{id}/season/{season}/episode/{seasonEpisode}"
    response_episode_data = requests.get(url_episode_data, headers=headers)
    episode_data = json.loads(response_episode_data.text)
    print(episode_data)
    episode_id = episode_data["id"] 

    if request.method == "GET":  

        favorite = db.execute("SELECT show_title, username FROM usershows WHERE episode_id = ? AND username = ?", episode_id, username[0]["username"]) 

        if favorite:
            print("episode exist")
            button_favorites = "remove from favorite episodes"
        else:
            print("episode does not exist")
            button_favorites = "add to favorite episodes"

        return render_template("episode.html", episode_data=episode_data, button_favorites=button_favorites)
    
    else:
        favorite = db.execute("SELECT show_title, username FROM usershows WHERE episode_id = ? AND username = ?", episode_id, username[0]["username"]) 
        
        button_favorites = "remove from favorite episodes"

        if not favorite:
            button_favorites = "add to favorite episodes"


        if request.form.get('favorite') == 'remove from favorite episodes':
            print("favorite")
            print("episode exist of favorite, I'll remove it")
            db.execute("DELETE FROM usershows WHERE episode_id = ? AND username = ?", episode_id, username[0]["username"]) 
            button_favorites = "add to favorite episodes"
        if request.form.get('favorite') == 'add to favorite episodes':
            print("episode does not exist on favorite, I'll add it")
            db.execute("INSERT INTO usershows (username, show_title, show_id, season_number, episode_number, episode_title, episode_id) VALUES (?, ?, ?, ?, ?, ?, ?)", username[0]["username"], show_title, id, episode_data["season_number"], episode_data["episode_number"], episode_data["name"], episode_data["id"])     
            button_favorites = "remove from favorite episodes"
                     
        else:
            print("no button clicked")

        return redirect(url_for("episode", id=id, season=season, seasonEpisode=seasonEpisode))

@app.route("/comparemovies", methods=["GET", "POST"])
def ajaxmovies():
    if request.method == "GET":
        return render_template("comparemovies.html")
    else:
        q = request.form.get("q")
        if q:
            url = f"https://api.themoviedb.org/3/search/movie?query={q}&page=1"

            print(url)
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                movies = json.loads(response.text)
                print(movies)
                return jsonify(movies)
    return jsonify({"error": "Invalid request"})

@app.route("/comparetvshows", methods=["GET", "POST"])
def ajaxshows():

    username = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])       

    if request.method == "GET":
        compare = db.execute("SELECT* FROM compareshows WHERE username = ?", username[0]["username"]) 
        print(compare)
        return render_template("comparetvshows.html", compare=compare)
    
    else:
        print("request method is post")
        q = request.form.get("q")
        if q:
            url = f"https://api.themoviedb.org/3/search/tv?query={q}&page=1"

            print(url)
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                shows = json.loads(response.text)
                print(shows)
                return jsonify(shows)
        
        if request.form.get("remove"):
            show_title = request.form.get("remove")
            print(show_title)
            db.execute("DELETE FROM compareshows WHERE show_title = ? AND username = ?", show_title, username[0]["username"]) 
            return redirect("/comparetvshows")

@app.route("/showratings", methods=["GET", "POST"])
def show_ratings():
    if request.method == "POST":
        print("request method is post")
        compare = []
        seasons_episodes_average_vote = []
        id = request.form.get("q")
        url = f"https://api.themoviedb.org/3/tv/{id}"
        response = requests.get(url, headers=headers)
        print(response.text)
        if response.status_code == 200:
            show_datas = json.loads(response.text)
            # print(movie_datas)
        show_title = show_datas["name"]


        # print(f"THIS IS SHOW DATAS {show_datas['name']}")
        number_of_seasons = show_datas["number_of_seasons"]
        print(f"There are {number_of_seasons} seasons")


        episodes_data = []

        counter = 0

        for season in range(number_of_seasons + 1):
            if season == 0:
                continue
            else:
                url_season_data = f"https://api.themoviedb.org/3/tv/{id}/season/{season}"
                response_season_data = requests.get(url_season_data, headers=headers)
                season_data = json.loads(response_season_data.text)
                print(season_data["name"])     
                episode_average_vote = []


                for episode in season_data["episodes"]:
                    counter = counter + 1
                    episodes_data.append(episode)
                    episode_average_vote.append(episode['vote_average'])

                # print(season_data["episodes"][0]["episode_number"])
                print(episode_average_vote)  
            seasons_episodes_average_vote.append(episode_average_vote)                      
            print(episode_average_vote)
            print(f"ALL VOTES FOR {show_title} ARE {seasons_episodes_average_vote}")
        return seasons_episodes_average_vote


@app.route("/toprated", methods=["GET"])
def top_rated():
    if request.method == "GET":
        pages = 11
        response_list = []
        for page in range(pages):
            url = f"https://api.themoviedb.org/3/movie/top_rated?language=en-US&page={page}"

            response = requests.get(url, headers=headers)
            movie_data = json.loads(response.text)
            response_list.append(movie_data)
        print(response_list)

        return render_template("toprated.html", response_list=response_list)

@app.route("/test", methods=["GET"])
def test():
    if request.method == "GET":
        # response_list = []
        # url = f"https://api.themoviedb.org/3/discover/movie"

        # response = requests.get(url, headers=headers)
        # movie_data = json.loads(response.text)
        # response_list.append(movie_data)
        # print(response_list)
        
        while True:
            random_movie_id = random.randint(1, 1200000)
            url_random_movie = f"https://api.themoviedb.org/3/movie/{random_movie_id}"
            response_random_movie = requests.get(url_random_movie, headers=headers)
            if response_random_movie:
                random_movie_data = json.loads(response_random_movie.text)
                if random_movie_data["adult"] != True:
                    print(f"ADULT CONTENT = {random_movie_data["adult"]}")
                    break
                else:
                    print(f"ADULT CONTENT = {random_movie_data}")
            else:
                print(f"URL NOT existent = {url_random_movie}")
            
        print(f"URL EXIT = {response_random_movie}")

        return render_template("test.html", movie=random_movie_data)

@app.route("/data", methods=["GET", "POST"])
def data():
    if request.method == "GET":
        favorites_list = []
        favorite_episodes_list = []

        users = db.execute("SElECT * FROM users")
        item_list = db.execute("SElECT * FROM favoriteswatchlist")
        episode_list = db.execute("SElECT * FROM usershows")
        episodes_ratings_list = db.execute("SElECT * FROM compareshows")
        print(f"favorites are {item_list}")
        print(f"favorite episodes are {episode_list}")

        for item in item_list:
            q = item["item_id"]
            if (item["type"] == "movie"):
                url = f"https://api.themoviedb.org/3/movie/{q}"
                response = requests.get(url, headers=headers)
                movie_data = json.loads(response.text)
                favorites_list.append(movie_data)
                print(movie_data["title"])

            elif(item["type"] == "tv-show"):
                url = f"https://api.themoviedb.org/3/tv/{q}"
                
            
                response = requests.get(url, headers=headers)
                movie_data = json.loads(response.text)
                favorites_list.append(movie_data)
                print(movie_data["name"])

        zip_list = zip(item_list, favorites_list) 

        for episode in episode_list:
            series_id = episode["show_id"]
            season_number = episode["season_number"]
            episode_number = episode["episode_number"]
            url = f"https://api.themoviedb.org/3/tv/{series_id}/season/{season_number}/episode/{episode_number}"
            response = requests.get(url, headers=headers)
            episode_data = json.loads(response.text)
            print(episode_data)
            favorite_episodes_list.append(episode_data)
            
        zip_list_episodes = zip(episode_list, favorite_episodes_list)

        return render_template ("data.html", users=users, favorites=item_list, favorites_list=favorites_list, zip_list=zip_list, favorite_episodes_list=favorite_episodes_list, zip_list_episodes=zip_list_episodes, episodes_ratings_list=episodes_ratings_list)
    
    else:
        remove_id = request.form.get("id")
        db.execute("DELETE FROM users WHERE id = ?", remove_id)
        return redirect ("/data")