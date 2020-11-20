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
  passive TEXT DEFAULT "Nothing",
  sex BOOLEAN DEFAULT FALSE,
  idUser INT NOT NULL,
  numQuest INT DEFAULT 1,
  numStep INT DEFAULT 1,
  FOREIGN KEY (idUser) REFERENCES user(idUser)
);

CREATE TABLE quest (
  questId INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  questNumber INTEGER UNIQUE NOT NULL,
  questName Text NOT NULL
);

CREATE TABLE step (
  stepNumber INT NOT NULL,
  textOfTheStep TEXT NOT NULL ,
  questId INT NOT NULL ,
  stepOptions TEXT NOT NULL ,
  FOREIGN KEY (questId) REFERENCES quest(questId)
);

INSERT INTO user(username,password)
VALUES
("theodore","$2b$12$wodx1pJqggHk7liJkwT22uLDMWxHBvp1lRGje.Ic05TISPPP5sRtm");

INSERT INTO hero(nameOfTheHero,lvl,weapon,armor,passive,sex,idUser)
VALUES
("My first hero", 1,"Epee",10,"Nothing",0,1);


INSERT INTO quest(questNumber, questName)
VALUES
(1, "It's the right gender ?!"),
(2, "Initial quest"),
(3, "Fight tutorial");

INSERT INTO step(questId, stepNumber, textOfTheStep, stepOptions)
VALUES
    (1, 1, "Your currently a |-sex_label|. Are you sure ? What's your sex ?", "female-female|male-male"),
    (1, 2, "Well you choose to be |-sex_label| for the rest of your life. Youre choice ... And so wath's for next ?", "walk-walk away|stay-stay"),
    (2, 1, "How, you still there ... Mmm, I have nothing for you. Just go !", "stay-stay|goto-go to aventure"),
    (2, 2, "I've understand ! You think I am one of this stange game PNJ ?", "yes-you look so|no-a what?"),
    (2, 3, "Mm, you know how to speak to me, to importante peaple. You must be reach in a great family ?", "no-Absolutly not|yes-Yes, I am sire"),
    (2, 4, "Because you seems to be honnest with me, let me give you a precious weapon! My stick !", "no-No thanks|yes-OMG so good"),
    (3, 1, "Oh, this way ! A savage fox name as 'chiper' just pass. Go and take back my stick !", "start-start fighting|run-run away"),
    (3, 2, "Fight","Chiper_the_fox"),
    (3, 3, "Nice, first fight ! You can keep the stick for your futur periple, know go.","home-go back home|garden-go walk in garden");