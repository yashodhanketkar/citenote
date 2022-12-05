CREATE TABLE users(
    id INTEGER PRIMARY KEY,
    username VARCHAR(255) UNIQUE,
    password VARCHAR(255),
    salt VARCHAR(255),
    role VARCHAR(255)
);