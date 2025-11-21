from cs50 import SQL

db = SQL("sqlite:///finalproject.db")

def is_favorite(user, item_id, type):
    rows = db.execute(
        "SELECT * FROM favoriteswatchlist" \
        "WHERE username=? AND" \
        "item_id=? AND" \
        "type=? AND" \
        "category = 'favorite'", 
        user, item_id, type
    )
    return len(rows) == 1


def add_favorite(user, item_id, type, title):
    db.execute(
        "INSERT INTO favoriteswatchlist (username, type, title, item_id, category)" \
        "VALUES(?, ?, ?, ?, 'favorite')",
        user, type, title, item_id
    )


def remove_favorite(user, item_id):
    db.execute(
        "DELETE FROM favoriteswatchlist WHERE username=? AND" \
        "item_id=? AND" \
        "category='favorite",
        user, item_id
    )

def get_username(user_id):
    result = db.execute("SELECT username FROM users WHERE id = ?", user_id)
    return result[0]["username"] if result else None