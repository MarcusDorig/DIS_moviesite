DROP TABLE IF EXISTS Users                CASCADE;
DROP TABLE IF EXISTS Favorites            CASCADE;
DROP TABLE IF EXISTS Movies               CASCADE;


CREATE TABLE Users(
  Username VARCHAR(25),
  Password VARCHAR(25) NOT NULL,
  PRIMARY KEY(Username)
);





commit;