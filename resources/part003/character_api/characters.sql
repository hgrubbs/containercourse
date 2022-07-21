DROP DATABASE IF EXISTS characters;
CREATE DATABASE characters;
USE characters;
CREATE TABLE users(id int primary key auto_increment not null, firstname text, lastname text);

INSERT INTO users(firstname, lastname) VALUES("Zaphod", "Beeblebrox");
INSERT INTO users(firstname, lastname) VALUES("Harry", "Tuttle");
INSERT INTO users(firstname, lastname) VALUES("Samwell", "Tarly");
