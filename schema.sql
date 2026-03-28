CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    hash TEXT NOT NULL
);

CREATE TABLE favoriteswatchlist (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL REFERENCES users(username) ON DELETE CASCADE,
    type TEXT NOT NULL,
    title TEXT NOT NULL,
    item_id INT NOT NULL,
    category TEXT NOT NULL CHECK (category IN ('favorite', 'watchlist')),
    personal_rating FLOAT
);

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
);

CREATE TABLE compareshows (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL REFERENCES users(username) ON DELETE CASCADE,
    show_title TEXT NOT NULL,
    episodes_ratings TEXT NOT NULL
);