from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from helpers.utils import tmdb_get, format_runtime
from helpers.dbQueries import *
import requests
import json
from helpers.utils import headers


user_bp = Blueprint("user", __name__)


@user_bp.route("/data", methods=["GET", "POST"])
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
    
    
@user_bp.route("/myarea", methods=["GET", "POST"])
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
    


