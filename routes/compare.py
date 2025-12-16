from flask import Blueprint, jsonify, render_template, request, redirect, url_for, session, flash
from helpers.dbQueries import *
from helpers.utils import tmdb_get, format_runtime

compare_bp = Blueprint("compare", __name__)


@compare_bp.route("/comparemovies", methods=["GET", "POST"])
def ajaxmovies():
    if request.method == "GET":
        return render_template("comparemovies.html")
    else:
        q = request.form.get("q")
        print("request form is", q)
        if q:
            compare_data = tmdb_get(f"search/movie?query={q}&page=1")
            # print("compare data: ", compare_data)

            return compare_data
    # return jsonify({"error": "Invalid request"})



# @compare_bp.route("/comparetvshows", methods=["GET", "POST"])
# def ajaxshows():

#     # username = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])       

#     if request.method == "GET":
#         # compare = db.execute("SELECT* FROM compareshows WHERE username = ?", username[0]["username"]) 
#         # print(compare)
#         return render_template("comparetvshows.html")
    
#     else:
#         print("request method is post")
#         q = request.form.get("q")
#         if q:
#             url = f"https://api.themoviedb.org/3/search/tv?query={q}&page=1"

#             print(url)
#             response = requests.get(url, headers=headers)

#             if response.status_code == 200:
#                 shows = json.loads(response.text)
#                 print(shows)
#                 return jsonify(shows)
        
        # if request.form.get("remove"):
        #     show_title = request.form.get("remove")
        #     print(show_title)
        #     db.execute("DELETE FROM compareshows WHERE show_title = ? AND username = ?", show_title, username[0]["username"]) 
        #     return redirect("/comparetvshows")