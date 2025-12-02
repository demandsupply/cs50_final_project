from flask import Blueprint, render_template, request, redirect, url_for, flash
from helpers.dbQueries import *
from helpers.utils import tmdb_get, format_runtime
from flask import session
# from app import login_required

movies_bp = Blueprint("movies", __name__)


@movies_bp.route("/movie/<id>", methods = ["GET", "POST"])
def movie(id):
    username = get_username(session["user_id"])
    movie_datas = tmdb_get(f"movie/{id}")
    if not movie_datas:
        return "Movie not found", 404
    
    print(f"movie id is {id}.\nIts data are {movie_datas}")

    imgMovie_datas = tmdb_get(f"movie/{id}/images?language=en")
    movie_datas["runtime_formatted"] = format_runtime(movie_datas.get("runtime"))

    if request.method == ("GET"):
        print("request method is get")
        
        button_favorites = "remove from favorites" if is_favorite(username, id, "movie") else "add to favorites"
        button_watchlist = "remove from watchlist" if is_in_watchlist(username, id, "movie") else "add to watchlist"

        return render_template ("movie.html", imgMovie_datas = imgMovie_datas,  movie_datas=movie_datas, button_favorites=button_favorites, button_watchlist=button_watchlist)


    else:
        print("request method is post")

        favorite_action = request.form.get('favorite')
        watchlist_action = request.form.get('watchlist')

        if favorite_action == "add to favorites":
            add_favorite(username, id, "movie", movie_datas["title"])
        elif favorite_action == "remove from favorites":
            remove_favorite(username, id)

        if watchlist_action == "add to watchlist":
            add_to_watchlist(username, id, "movie", movie_datas["title"])
        elif watchlist_action == "remove from watchlist":
            remove_from_watchlist(username, id)


        return redirect(url_for("movies.movie", id=id))
