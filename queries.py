import psycopg2


class Queries:
    # On initialisation we connect once to the DB
    def __init__(self):
        self.connect = psycopg2.connect("dbname='moviedb' user='postgres' host='localhost' password='Yvk89wkd'")


    def ResetDB(self):
        cur = self.connect.cursor()
        cur.execute(open('Schemas.sql', 'r').read())
        cur.close()
        cur2 = self.connect.cursor()
        with open('moviedata_cleaned', 'r') as f:
            next(f)
            cur2.copy_from(f, 'movies', sep=';')
        self.connect.commit()
        cur2.execute(open('users.sql','r').read())
        self.connect.commit()
        cur2.close()

    

    def lookupUser(self, user, password):
        cur = self.connect.cursor()
        cur.execute("""SELECT * FROM Users WHERE Username=%s AND password=%s""",(user, password))
        lst = cur.fetchall()
        cur.close()
        return lst
    


    def addUser(self, user, password):
        cur = self.connect.cursor()
        cur.execute("""SELECT * FROM Users WHERE Username=%s""",(user,))
        lst = cur.fetchall()
        if len(lst) > 0:
            return 0
        else:
          cur.execute("INSERT INTO Users VALUES (%s,%s)",(user, password))
          self.connect.commit()
          cur.close()
          return 1
        
    def deleteUser(self, user, password):
        cur = self.connect.cursor()
        cur.execute("""DELETE FROM Users WHERE Username=%s AND Password=%s""",(user, password))
        self.connect.commit()
        cur.close()
    
    def lookupMovie(self, id):
        cur = self.connect.cursor()
        cur.execute("""SELECT * FROM Movies WHERE ID=%s""",(id,))
        lst = cur.fetchone()
        cur.close()
        return lst
    

    def searchMovies(self, ts, rs, gs):
        cur = self.connect.cursor()
        cur.execute("""SELECT Movies.ID,Movies.Genre,Movies.Title FROM Movies
        WHERE (%(title)s='' OR Movies.Title LIKE %(title)s)
        AND (%(gen)s LIKE '2' OR Movies.Genre LIKE %(gen)s)
        AND ( 8 IN %(rated)s OR Movies.ID IN (SELECT M_id FROM Ratings GROUP BY M_id HAVING ROUND(AVG(Rating),0) IN %(rated)s))
        GROUP BY Movies.ID""",{'title':ts, 'gen': gs, 'rated': tuple(rs)})
        lst = cur.fetchall()
        cur.close()
        return lst




    def insertRating(self, rating, m_id, u_id):
        cur = self.connect.cursor()
        cur.execute("""SELECT * FROM Ratings WHERE U_id=%s AND M_id=%s""",(u_id, m_id))
        lst = cur.fetchone()
        if lst == None:
            cur.execute("INSERT INTO Ratings VALUES (%s, %s, %s)", (rating, m_id, u_id))
            self.connect.commit()
            cur.close()
            return
        else:
            cur.execute("""UPDATE Ratings SET Rating=%s
            WHERE U_id=%s AND M_id=%s""",(rating, u_id, m_id))


    # While not being able to implement this, having the personal rated and favorite
    # lists as views makes more complicated searching and filtering simpler to query
    def ratedMovies(self, u_id):
        cur = self.connect.cursor()
        cur.execute("""CREATE OR REPLACE VIEW Userrated AS
        SELECT ID,Title FROM Movies
         INNER JOIN Ratings ON Movies.ID = Ratings.M_id
         WHERE Ratings.U_id = %s;
         SELECT * FROM Userrated""",(u_id,))
        lst = cur.fetchall()
        cur.close()
        return lst
    
    def NsearchRate(self, input):
        cur=self.connect.cursor()
        cur.execute("""SELECT * FROM Userrated WHERE Title LIKE %s""",(input,))
        lst = cur.fetchall()
        cur.close()
        return lst

    def deleteRating(self, rating, m_id, u_id):
        cur = self.connect.cursor()
        cur.execute("""DELETE FROM Ratings WHERE rating=%s AND m_id=%s AND u_id=%s""",(rating, m_id, u_id))
        self.connect.commit()
        cur.close()


    def insertFavorite(self, u_id, m_id):
        cur = self.connect.cursor()
        cur.execute("SELECT * FROM Favorites WHERE ID=%s AND M_id=%s", (u_id, m_id))
        lst = cur.fetchone()
        if lst != None:
            cur.close()
            return
        else:
            cur.execute("""INSERT INTO Favorites VALUES (%s,%s)""",(u_id, m_id))
            self.connect.commit()
        cur.close()
        return 
    
    def checkFavorite(self, u_id, m_id):
        cur = self.connect.cursor()
        cur.execute("SELECT * FROM Favorites WHERE ID=%s AND M_id=%s", (u_id, m_id))
        lst = cur.fetchone()
        return lst


    def getFavList(self, u_id):
        cur = self.connect.cursor()
        cur.execute("""CREATE OR REPLACE VIEW UserFav AS
                    SELECT DISTINCT Movies.ID,Title FROM Movies 
                    INNER JOIN FAVORITES ON Movies.ID IN (SELECT M_id FROM Favorites WHERE ID=%s);
                    SELECT * FROM UserFav""", (u_id,))
        lst = cur.fetchall()
        cur.close()
        return lst
    
    def NsearchFav(self, input):
        cur=self.connect.cursor()
        cur.execute("""SELECT * FROM Userfav WHERE Title LIKE %s""",(input,))
        lst = cur.fetchall()
        cur.close()
        return lst


    def deleteFavorite(self, u_id, m_id):
        cur = self.connect.cursor()
        cur.execute("DELETE FROM Favorites WHERE ID=%s AND m_id=%s",(u_id, m_id))
        self.connect.commit()
        cur.close()

    def newestMovies(self):
        cur = self.connect.cursor()
        cur.execute("""SELECT ID,genre,release_date,title FROM Movies
        ORDER BY release_date DESC
        FETCH FIRST 10 ROWS ONLY""")
        lst = cur.fetchall()
        cur.close()
        return lst
    
    def getMovieRatings(self, movie):
        cur = self.connect.cursor()
        cur.execute("""SELECT Ratings.Rating, U_id FROM Ratings
        WHERE M_id = %s""",(movie,))
        lst = cur.fetchall()
        cur.close()
        return lst
    

    def getAvgRating(self, movie):
        cur = self.connect.cursor()
        cur.execute("""SELECT ROUND(AVG(Ratings.Rating),1) FROM Ratings
        WHERE M_id = %s""",(movie,))
        lst = cur.fetchone()
        cur.close()
        return lst

  
