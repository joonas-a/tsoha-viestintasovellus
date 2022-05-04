CREATE TABLE Users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    is_admin BOOLEAN
);
CREATE TABLE Boards (
    id SERIAL PRIMARY KEY,
    title TEXT
);
CREATE TABLE Threads (
    id SERIAL PRIMARY KEY,
    content TEXT,
    u_id INTEGER REFERENCES Users,
    b_id INTEGER REFERENCES Boards,
    created_at TIMESTAMP,
    title TEXT
);
INSERT INTO Boards (title) VALUES ('main');

INSERT INTO Boards (title) VALUES ('school');