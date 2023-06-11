DROP TABLE IF EXISTS Users                CASCADE;
DROP TABLE IF EXISTS Favorites            CASCADE;
DROP TABLE IF EXISTS Movies               CASCADE;
DROP TABLE IF EXISTS Ratings              CASCADE;


CREATE TABLE Users(
  Username VARCHAR(25),
  Password VARCHAR(25) NOT NULL,
  PRIMARY KEY(Username)
);

CREATE TABLE Movies(
  ID INT,
  Budget BIGINT,
  Genre TEXT,
  original_language TEXT,
  release_date DATE,
  Revenue BIGINT,
  Runtime FLOAT,
  Title VARCHAR(255),
  PRIMARY KEY(ID)
);

CREATE TABLE Ratings(
  Rating INT, 
  CHECK (0 <= Rating  AND Rating <= 5),
  M_id INT,
  U_id VARCHAR(25),
  PRIMARY KEY(M_id, U_id),
  FOREIGN KEY(M_id) REFERENCES Movies(ID) ON DELETE CASCADE,
  FOREIGN KEY(U_id) REFERENCES Users(Username) ON DELETE CASCADE
);


CREATE TABLE Favorites(
  ID VARCHAR(255),
  M_id INT,
  PRIMARY KEY(ID, M_id),
  FOREIGN KEY(ID) REFERENCES Users(Username) ON DELETE CASCADE,
  FOREIGN KEY(M_id) REFERENCES Movies(ID) ON DELETE CASCADE
);





commit;