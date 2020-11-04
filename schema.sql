DROP TABLE IF EXISTS user;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

INSERT INTO user(username,password)
VALUES
("theodore","password"),
("theodore2","$2b$12$wodx1pJqggHk7liJkwT22uLDMWxHBvp1lRGje.Ic05TISPPP5sRtm");