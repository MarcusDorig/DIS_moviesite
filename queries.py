import psycopg2
import csv
import numpy as np
import pandas as pd


class Queries:
    # On initialisation we connect once to the DB
    def __init__(self):
        self.connect = psycopg2.connect("dbname='moviedb' user='postgres' host='localhost' password='Yvk89wkd'")

    def ResetDB(self):
        cur = self.connect.cursor()
        cur.execute(open('Schemas.sql', 'r').read())
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
        data.to_csv('moviedata_cleaned', sep=',', index_label='id')
        
        cur.close()

    

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
    

