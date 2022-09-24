import sqlite3
from sqlite3 import Error

class Model():



    def create_connection(path):
        connection = None

        try:
            connection = sqlite3.connect(path)
            print("Connection successful.")
        except Error as e:
            print("Error " + e + " with connecting to path.")

        return connection

    def execute_query(connection, query):
        cursor = connection.cursor()

        try:
            cursor.execute(query)
            connection.commit()
            print("Query executed.")
        except Error as e:
            print("Error " + e + " occurred when executing query.")

    create_users_table = """CREATE TABLE IF NOT EXISTS users (
        id INT AUTOINCREMENT,

        username TEXT NOT NULL,
        password TEXT NOT NULL, 

        time INT NOT NULL,
        budget INT NOT NULL

    )
    """

    create_user_cuisine_table = """CREATE TABLE IF NOT EXISTS user_cuisine
        id INT AUTOINCREMENT,
        cuisine_name INT NOT NULL,
        cuisine_name_2 INT NOT NULL,
        cuisine_name_3 INT NOT NULL
    """

    create_user_ingredients_table = """CREATE TABLE IF NOT EXISTS user_ingredients
    
    """
    
    create_recipes_table = """CREATE TABLE IF NOT EXISTS recipes (
        id INT AUTOINCREMENT,
        rating INT, 
        time INT,
        cost INT,
        cuisine TEXT NOT NULL
    )"""

    recipes_ingredients_table = """CREATE TABLE IF NOT EXISTS recipes_ingredients (
        id INT AUTOINCREMENT,
        ingredient_name TEXT NOT NULL,
        quantity INT NOT NULL
    )
    """

    #def add_user(self, username,     



    
