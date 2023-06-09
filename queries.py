import psycopg2
import csv
import numpy as np
import pandas as pd


class Queries:
    # On initialisation we connect once to the DB
    def __init__(self):
        self.connect = psycopg2.connect("dbname='moviedb' user='postgres' host='localhost' password='Yvk89wkd'")

    def clean_data(self):
        data = pd.read_csv(open("C:/Users/marcu/OneDrive/Dokumenter/Datalogi/DIS/moviedata2/tmdb_5000_movies.csv", encoding='utf8'), 
                               delimiter=',')
        data.drop('homepage', inplace=True, axis=1)
        data.drop('id', inplace=True, axis=1)
        data.drop('keywords', inplace=True, axis=1)
        data.drop('overview', inplace=True, axis=1)
        data.drop('popularity', inplace=True, axis=1)
        data.drop('production_companies', inplace=True, axis=1)
        data.drop('production_countries', inplace=True, axis=1)
        data.drop('spoken_languages', inplace=True, axis=1)
        data.drop('status', inplace=True, axis=1)
        data.drop('tagline', inplace=True, axis=1)
        data.drop('vote_average', inplace=True, axis=1)
        data.drop('vote_count', inplace=True, axis=1)
        data.drop('title', inplace=True, axis=1)
        data.to_csv('moviedata_cleaned', sep=';', index_label='id')

    def ResetDB(self):
        cur = self.connect.cursor()
        cur.execute(open('Schemas.sql', 'r').read())
        cur.close()
        cur2 = self.connect.cursor()
        with open('moviedata_cleaned', 'r', encoding='utf8') as f:
            next(f)
            cur2.copy_from(f, 'movies', sep=';')
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
    
    def lookupMovie(self, budget, genre, original_language, title, release_date, revenue, runtime, id):
        cur = self.connect.cursor()
        cur.execute("""SELECT * FROM Movies""")
        lst = cur.fetchall()
        cur.close()
        return lst

    def insertRating(self, rating, m_id, u_id):
        cur = self.connect.cursor()
        cur.execute("INSERT INTO Ratings VALUES (%s, %s, %s)", (rating, m_id, u_id))
        self.connect.commit()
        cur.close()

    def lookupRating(self, rating, m_id, u_id):
        cur = self.connect.cursor()
        cur.execute("""SELECT * FROM Ratings WHERE rating=%s AND m_id=%s AND u_id=%s""",(rating, m_id, u_id))
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
        cur.execute("INSERT INTO Favorites VALUES (%s, %s)", (u_id, m_id))
        self.connect.commit()
        cur.close()    

    def lookupFavorites(self, u_id):
        cur = self.connect.cursor()
        cur.execute("""SELECT * FROM Movies 
                     INNER JOIN FAVORITES ON Movies.ID=(SELECT M_id FROM Favorites WHERE u_id=%s)""", (u_id))
        lst = cur.fetchall()
        cur.close()
        return lst

    def deleteFavorite(self, u_id, m_id):
        cur = self.connect.cursor()
        cur.execute("DELETE FROM Favorites WHERE u_id=%s AND m_id=%s",(u_id, m_id))
        self.connect.commit()
        cur.close()

    def newestMovies(self):
        cur = self.connect.cursor()
        cur.execute("""SELECT title,genre,release_date FROM Movies
        ORDER BY release_date DESC
        FETCH FIRST 15 ROWS ONLY""")
        lst = cur.fetchall()
        cur.close()
        return lst

