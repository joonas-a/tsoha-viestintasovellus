CREATE TABLE Users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    is_admin BOOLEAN,
);
CREATE TABLE Boards (
    id SERIAL PRIMARY KEY,
    title TEXT
);