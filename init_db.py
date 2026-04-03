import os
from dotenv import load_dotenv
from cs50 import SQL

load_dotenv()

# db = SQL(
#     f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
#     f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
# )

db = SQL(os.getenv("DATABASE_URL"))

tables = ["compareshows", "usershows", "favoriteswatchlist", "users"]
for table in tables:
    db.execute(f"DROP TABLE IF EXISTS {table} CASCADE")

db.execute("""
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    hash TEXT NOT NULL
)
""")

db.execute("""
CREATE TABLE favoriteswatchlist (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL REFERENCES users(username) ON DELETE CASCADE,
    type TEXT NOT NULL,
    title TEXT NOT NULL,
    item_id INT NOT NULL,
    category TEXT NOT NULL CHECK (category IN ('favorite','watchlist')),
    personal_rating FLOAT
)
""")

db.execute("""
CREATE TABLE usershows (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL REFERENCES users(username) ON DELETE CASCADE,
    show_title TEXT NOT NULL,
    show_id INT NOT NULL,
    season_number INT NOT NULL,
    episode_number INT NOT NULL,
    episode_title TEXT NOT NULL,
    episode_id INT NOT NULL,
    personal_rating FLOAT
)
""")

db.execute("""
CREATE TABLE compareshows (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL REFERENCES users(username) ON DELETE CASCADE,
    show_title TEXT NOT NULL,
    episodes_ratings TEXT NOT NULL
)
""")