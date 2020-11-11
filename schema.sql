DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS hero;
DROP TABLE IF EXISTS questBook;
DROP TABLE IF EXISTS quest;
DROP TABLE IF EXISTS step;

CREATE TABLE user (
  idUser INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE hero (
  idHero INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  nameOfTheHero TEXT UNIQUE NOT NULL,
  lvl INT DEFAULT 1,
  weapon TEXT DEFAULT "Hands",
  armor INT DEFAULT 0,
  passive TEXT DEFAULT "None",
  sex BOOLEAN DEFAULT FALSE,
  idUser INT NOT NULL,
  numQuest INT DEFAULT 1,
  numStep INT DEFAULT 1,
  FOREIGN KEY (idUser) REFERENCES user(idUser)
);

CREATE TABLE quest (
  questId INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  nameOfTheQuest TEXT
);

CREATE TABLE step (
  stepNumber INT NOT NULL,
  textOfTheStep TEXT DEFAULT "Text of the step isn't set yet",
  questId INT,
  FOREIGN KEY (questId) REFERENCES quest(questId)
);

INSERT INTO user(username,password)
VALUES
("theodore","$2b$12$wodx1pJqggHk7liJkwT22uLDMWxHBvp1lRGje.Ic05TISPPP5sRtm");

INSERT INTO hero(nameOfTheHero,lvl,weapon,armor,passive,sex,idUser)
VALUES
("My first hero", 1,"Epee",10,"Nothing",0,1);


INSERT INTO quest(nameOfTheQuest)
VALUES
("The first quest"),
("The second quest"),
("The third quest");

INSERT INTO step(textOfTheStep,questId,stepNumber)
VALUES
("The step 0 of the first quest",1,0),
("The step 1 of the first quest",1,1),
("The step 0 of the second quest",2,0),
("The step 1 of the second quest",2,1),
("The step 0 of the third quest",3,0),
("The step 1 of the third quest",3,1);