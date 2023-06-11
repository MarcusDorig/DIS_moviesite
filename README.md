# Movie database

Running the project:

- Create an empty postgres database and make sure that the information written in queries.py when calling psycopg2.connect matches
  such that it connects to this database, if you create the database via the psql terminal then you will write the values you need
  when logging into user postgres

- Initialize the database, by running the SQL files (Creating the necessary tables)
  
  $ python Initialize_database.py

- Run the web-application
  
  $ python website.py


Navigating the application:

- It's optional whether you want to login or not, although you should be aware that some features are only available when logged in. 

- You can login by either creating a new user or using the following:


  username: user1 


  password: user1password
