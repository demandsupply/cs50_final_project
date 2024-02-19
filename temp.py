from cs50 import SQL

# with open('IMDB-movies.csv', 'r') as file:
#     for row in file:
#         print(row)

db = SQL("sqlite:///movies.db")

temp = db.execute("SELECT * FROM movies LIMIT 50")
print(temp)