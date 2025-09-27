# Make a connection from DB Harvard
import mysql.connector
import requests 
from mysql.connector import Error

def get_connection():
    connection = None
    try:
        # setting the database connection with details
        connection = mysql.connector.connect(
            host = '127.0.0.1',
            user = 'root',
            password = 'Admin@#$123', 
            database = 'harvard'
        )

        # check connection to mysql is connected or not
        if connection.is_connected():
            cursor = connection.cursor()
            print("Connection to mysql is connected.")

    except Error as e:
            print(" Getting error while Connection to mysql.")

    #finally:
     #   if connection.is_connected():
      #      if connection.close():
       #         print("Mysql connection close.")
    return connection             
        

