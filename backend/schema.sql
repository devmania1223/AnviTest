CREATE TABLE
IF NOT EXISTS accounts
(
    id integer PRIMARY KEY,
    email text NOT NULL,
    password text NOT NULL
);