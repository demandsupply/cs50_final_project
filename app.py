import os
from flask import Flask, redirect, render_template, request, jsonify, session, flash, url_for
from cs50 import SQL
from flask_session import Session
import requests
import json
# import param
import random
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
from config import AUTH_CODE
import ast
from helpers.utils import headers, tmdb_get, format_runtime
from helpers.dbQueries import (
    is_favorite, add_favorite, remove_favorite,
    get_username,
    is_in_watchlist, add_to_watchlist, remove_from_watchlist,
    is_favorite_episode, add_favorite_episode, remove_favorite_episode
)
from urllib.parse import urlencode

from routes.movies import movies_bp
from routes.shows import shows_bp
from routes.auth import auth_bp, login_required
from routes.topRateds import top_rateds_bp


# Configure application
app = Flask(__name__)


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Configure sql database
db = SQL("sqlite:///finalproject.db")


app.register_blueprint(movies_bp)
app.register_blueprint(shows_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(top_rateds_bp)



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






#############################   INDEX    ############################

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        popular_movie_list = []
        popular_show_list = []

        # fetch data using function from helpers -> more efficient
        popular_movies = tmdb_get(f"movie/popular")

        popular_movie_list = popular_movies["results"]
        print("popular_movie_list: ", popular_movie_list)

        # kept old code for comparison
        show_url = f"https://api.themoviedb.org/3/tv/popular"

        response_show = requests.get(show_url, headers=headers)
        show_data = json.loads(response_show.text)
        popular_show_list.append(show_data)
        # print("popular_show_list", popular_show_list)

        # get random movies using "discover/movie?" endpoint -> lighter and more efficient way
        def get_random_movie():
            params = {
                "adult": "false",
                "page": random.randint(1, 200)
            }

            data = tmdb_get("discover/movie?" + urlencode(params))

            if not data or "results" not in data:
                return None
            
            return random.choice(data["results"])

        # original code to get random shows 
        while True:
            random_show_id = random.randint(1, 400000)
            url_random_show = f"https://api.themoviedb.org/3/tv/{random_show_id}"
            response_random_show = requests.get(url_random_show, headers=headers)
            if response_random_show:
                random_show_data = json.loads(response_random_show.text)
                if random_show_data["adult"] != True:
                    break
                else:
                    print(f"Adult content, load another show")
            else:
                print(f"Show does not exist, load another ID")        
            
        return render_template("index.html", popular_movie_list=popular_movie_list, popular_show_list=popular_show_list, random_movie=get_random_movie(), random_show=random_show_data)
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
@login_required
def search():
    if request.method == "POST":
        query = request.form.get("query")
        if not query:
            flash("Insert a search")
            return redirect("/search")

        params = urlencode({"query": query})
        data = tmdb_get("search/multi?" + params)

        results = data.get("results", []) if data else []

        return render_template("search.html", results=results, query=query)

    return render_template("search.html", results=None)








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

    # username = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])       

    if request.method == "GET":
        # compare = db.execute("SELECT* FROM compareshows WHERE username = ?", username[0]["username"]) 
        # print(compare)
        return render_template("comparetvshows.html")
    
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
        
        # if request.form.get("remove"):
        #     show_title = request.form.get("remove")
        #     print(show_title)
        #     db.execute("DELETE FROM compareshows WHERE show_title = ? AND username = ?", show_title, username[0]["username"]) 
        #     return redirect("/comparetvshows")

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
                movie_data = tmdb_get(f"movie/{q}")
                favorites_list.append(movie_data)

            elif(item["type"] == "tv-show"):
                movie_data = tmdb_get(f"tv/{q}")
                favorites_list.append(movie_data)

        zip_list = zip(item_list, favorites_list) 

        for episode in episode_list:
            series_id = episode["show_id"]
            season_number = episode["season_number"]
            episode_number = episode["episode_number"]

            episode_data = tmdb_get(f"tv/{series_id}/season/{season_number}/episode/{episode_number}")
            favorite_episodes_list.append(episode_data)
            
        zip_list_episodes = zip(episode_list, favorite_episodes_list)

        return render_template ("data.html", 
                                users=users, 
                                favorites=item_list, 
                                favorites_list=favorites_list, 
                                zip_list=zip_list, 
                                favorite_episodes_list=favorite_episodes_list, 
                                zip_list_episodes=zip_list_episodes, 
                                episodes_ratings_list=episodes_ratings_list
                                )
    
    else:
        remove_id = request.form.get("id")
        db.execute("DELETE FROM users WHERE id = ?", remove_id)
        return redirect ("/data")
    
@app.route("/myarea", methods=["GET", "POST"])
def myarea():
    if request.method == "POST":
        print("request method is post")

        usernameToFix = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])
        username = usernameToFix[0]["username"]

        id_favorite = request.form.get("movie_id_favorite")
        print("tv-show exist of favorite, I'll remove it")
        db.execute("DELETE FROM favoriteswatchlist WHERE item_id = ? AND category = 'favorite' AND username = ?", id_favorite, username) 

        id_watchlist = request.form.get("movie_id_watchlist")
        db.execute("DELETE FROM favoriteswatchlist WHERE item_id = ? AND category = 'watchlist' AND username = ?", id_watchlist, username) 

        id_favorite_episode = request.form.get("episode_id_favorite")
        db.execute("DELETE FROM usershows WHERE episode_number = ? AND username = ?", id_favorite_episode, username) 

        return redirect ("myarea")
    else:
        favorites_list = []
        watchlist_list = []
        favorite_episodes_list = []

        usernameToFix = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])
        username = usernameToFix[0]["username"]       
        item_list = db.execute("SElECT * FROM favoriteswatchlist WHERE username = ?", username)
        episode_list = db.execute("SElECT * FROM usershows WHERE username = ?", username)
        episodes_ratings_list = db.execute("SElECT * FROM compareshows WHERE username = ?", username)
        print(f"favorites are {item_list}")
        print(f"favorite episodes are {episode_list}")

        for item in item_list:
            q = item["item_id"]
            if (item["type"] == "movie"):
                url = f"https://api.themoviedb.org/3/movie/{q}"
                response = requests.get(url, headers=headers)
                movie_data = json.loads(response.text)

                if(item["category"] == "favorite"):
                    favorites_list.append(movie_data)
                else:
                    watchlist_list.append(movie_data)

            elif(item["type"] == "tv-show"):
                url = f"https://api.themoviedb.org/3/tv/{q}"
                response = requests.get(url, headers=headers)
                movie_data = json.loads(response.text)

                if(item["category"] == "favorite"):
                    favorites_list.append(movie_data)
                else:
                    watchlist_list.append(movie_data)

                
        zip_list_favorites = zip(item_list, favorites_list) 
        zip_list_watchlist = zip(item_list, watchlist_list) 

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
        if item_list:
            print("movie exist")
            button_favorites = "remove from favorites"
        else:
            print("movie does not exist")
            button_favorites = "add to favorites"


        return render_template("myarea.html", button_favorites=button_favorites, users=username, favorites=item_list, favorites_list=favorites_list, watchlist_list=watchlist_list, zip_list_favorites=zip_list_favorites, zip_list_watchlist=zip_list_watchlist, favorite_episodes_list=favorite_episodes_list, zip_list_episodes=zip_list_episodes, episodes_ratings_list=episodes_ratings_list)
    


