import os
from flask import Flask, redirect, render_template, request
from cs50 import SQL
import requests
import json

# Configure application
app = Flask(__name__)



headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI3Yjg3YzFlNzU4ZTNkNzA4YzUyMmUyYmUyN2FjYjBhMCIsInN1YiI6IjY1Y2U3MzM0YTMxNDQwMDE2MmE2ZGMwZCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.Azo3xqnhGWGHEv7B_Genf96HVFJcEBfJki1_vZBN0W0"
}



@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        movie = request.args.get("movie")
        print(movie)

        url = "https://api.themoviedb.org/3/search/movie?query={0}".format(movie)

        print(url)
        response = requests.get(url, headers=headers)
        json_response = json.loads(response.text)
        print(response.text)
        print("THOSE ARE")
        print(json_response["results"])


        return render_template("index.html", movie=movie, response=response, json_response=json_response["results"])
    else:
        movie = request.form.get("movie")
        print(movie)
        return redirect("/")
