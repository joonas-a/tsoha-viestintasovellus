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
    t_id INTEGER REFERENCES Threads ON DELETE CASCADE,
    u_id INTEGER REFERENCES Users,
    created_at TIMESTAMP,
    content TEXT
);
CREATE TABLE if not exists Comment_Votes (
    id SERIAL PRIMARY KEY,
    vote SMALLINT,
    u_id INTEGER REFERENCES Users,
    c_id INTEGER REFERENCES Comments ON DELETE CASCADE
);
CREATE TABLE if not exists Thread_Votes (
    id SERIAL PRIMARY KEY,
    vote SMALLINT,
    u_id INTEGER REFERENCES Users,
    t_id INTEGER REFERENCES Threads ON DELETE CASCADE
);
