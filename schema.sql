CREATE TABLE if not exists Users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    is_admin BOOLEAN
);
CREATE TABLE if not exists Boards (
    id SERIAL PRIMARY KEY,
    title TEXT
);
CREATE TABLE if not exists Threads (
    id SERIAL PRIMARY KEY,
    content TEXT,
    u_id INTEGER REFERENCES Users,
    b_id INTEGER REFERENCES Boards,
    created_at TIMESTAMP,
    title TEXT
);
CREATE TABLE if not exists Comments (
    id SERIAL PRIMARY KEY,
    t_id INTEGER REFERENCES Threads,
    u_id INTEGER REFERENCES Users,
    created_at TIMESTAMP,
    content TEXT
);
