import os
from flask import Flask, redirect, render_template, request
from cs50 import SQL
import requests
import json
import param

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
        limit = 200
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

    

        # response2 = requests.get {
        #     "https://api.themoviedb.org/3/search/movie", 
        #     params = {
                
        #     }
        # }

    else:
        movie = request.form.get("movie")
        print(movie)
        return redirect("/")
