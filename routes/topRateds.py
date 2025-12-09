from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from helpers.utils import tmdb_get, format_runtime


top_rateds_bp = Blueprint("toprated", __name__)


@top_rateds_bp.route("/toprated", methods=["GET"])
def top_rated():
    if request.method == "GET":
        pages = 11
        response_list = []

        for page in range(pages):
            movie_data = tmdb_get(f"movie/top_rated?language=en-US&page={page}")
            if movie_data:
                response_list.append(movie_data)
        print("Top 200 movies: ", response_list)

        return render_template("toprated.html", response_list=response_list)


@top_rateds_bp.route("/topratedshows", methods=["GET"])
def top_rated_shows():
    if request.method == "GET":
        pages = 6
        response_list = []

        for page in range(pages):
            show_data = tmdb_get(f"tv/top_rated?language=en-US&page={page}")
            if show_data:
                response_list.append(show_data)
        print("Top 200 movies: ", response_list)

        return render_template("topratedshows.html", response_list=response_list)
