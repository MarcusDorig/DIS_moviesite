import psycopg2


class Queries:
    # On initialisation we connect once to the DB
    def __init__(self):
        self.connect = psycopg2.connect("dbname='moviedb' user='postgres' host='localhost' password='Yvk89wkd'")

    def ResetDB(self):
        cur = self.connect.cursor()
        cur.execute(open('Schemas.sql', 'r').read())
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
    

