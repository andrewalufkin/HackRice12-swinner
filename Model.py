import sqlite3
from sqlite3 import Error

class Model():

    def __init__(self):
        connection = self.create_connection("E:\\sm_app.sqlite")

        cursor = connection.cursor()

        cursor.execute(self.create_users_table)
        cursor.execute(self.create_user_cuisine_table)
        cursor.execute(self.create_user_ingredients_table)
        cursor.execute(self.create_recipes_table)
        cursor.execute(self.recipes_ingredients_table)

        self.print_table(connection, "users")
        self.print_table(connection, "user_cuisine")
        self.print_table(connection, "user_ingredients")
        self.print_table(connection, "recipes")
        self.print_table(connection, "recipes_ingredients")

    def create_connection(self, path):
        connection = None

        try:
            connection = sqlite3.connect(path)
            print("Connection successful.")
        except Error as e:
            print("Error " + e + " with connecting to path.")

        return connection

    def execute_query(self, connection, query):
        cursor = connection.cursor()

        try:
            cursor.execute(query)
            connection.commit()
            print("Query executed.")
        except Error as e:
            print("Error " + str(e) + " occurred when executing query.")

    def initiate_tables(self, connection):
        self.execute_query(connection, self.create_users_table)
        self.execute_query(connection, self.create_user_cuisine_table)
        self.execute_query(connection, self.create_user_ingredients_table)
        self.execute_query(connection, self.create_recipes_table)
        self.execute_query(connection, self.recipes_ingredients_table)

    #create_users_table = """
     #   CREATE TABLE IF NOT EXISTS users (
      #  id INTEGER PRIMARY KEY AUTOINCREMENT,
       # name TEXT NOT NULL,
        #age INTEGER,
        #gender TEXT,
        #nationality TEXT
        #);""" 
        
    create_users_table = """CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,

        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL, 

        time INTEGER,
        budget INTEGER

    );"""

    create_user_cuisine_table = """CREATE TABLE IF NOT EXISTS user_cuisine (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cuisine_name INT NOT NULL,
        cuisine_name_2 INT NOT NULL,
        cuisine_name_3 INT NOT NULL
    );"""

    create_user_ingredients_table = """CREATE TABLE IF NOT EXISTS user_ingredients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ingredient_name INTEGER,
        ingredient_name_2 INTEGER,
        ingredient_name_3 INTEGER
    );"""
    
    create_recipes_table = """CREATE TABLE IF NOT EXISTS recipes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        rating INTEGER, 
        time INTEGER,
        cost INTEGER,
        cuisine TEXT NOT NULL
    );"""

    recipes_ingredients_table = """CREATE TABLE IF NOT EXISTS recipes_ingredients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ingredient_name TEXT NOT NULL,
        quantity INTEGER NOT NULL
    );"""

    def add_user(self, connection, username, password, cuisine, dietary_restrictions, time, budget):

        

        add_user = """INSERT_INTO
        users(username, password, time, budget) VALUES (?, ?, ?, ?)"""

        args = (username, password, time, budget)

        query = [add_user, args]

        existing_cuisines = """SELECT * FROM user_cuisine
        """

        cuisines = self.execute_query(connection, existing_cuisines)

        for cuisine_type in cuisine:
            if cuisine_type not in cuisines:
                #args = (cuisine_type, 1)
                args = (1, )
                self.execute_query(connection, ["""ALTER TABLE user_cuisine
                ADD Southern (?)""", args])

            else:
                #args = (cuisine_type, 1)
                args = (1, )
                self.execute_query(connection, ["""INSERT INTO user_cuisine 
                Peppers VALUES (?)""", args])

        existing_restrictions = """SELECT * FROM user_ingredients
        """
        
        restrictions = self.execute_query(connection, existing_restrictions)

        for ingredient in dietary_restrictions:
            if ingredient not in restrictions:
                #args = (ingredient, 1) #1 means they are allergic
                args = (1, )
                self.execute_query(connection, ["""ALTER TABLE user_cuisine
                ADD Peppers (?)""", args])

            else:
                #args = (ingredient, 1)
                args = (1, )
                self.execute_query(connection, ["""INSERT INTO user_cuisine 
                Peppers VALUES (?)""", args])

        self.execute_query(connection, query)

    def delete_user(self, connection, username):
        id_to_delete = """SELECT id FROM users
        WHERE username = (?)
        """
        args = (username)

        query = [id_to_delete, args]

        id = self.execute_query(connection, query)

        delete_cuisine = """DELETE FROM user_cuisine
        WHERE id = (?)"""

        delete_ingredients = """DELETE FROM user_ingredients
        WHERE id = (?)"""

        self.execute_query(connection, [delete_cuisine, id])
        self.execute_query(connection, [delete_ingredients, id])

    def print_table(self, connection, table_name):
        
        get_whole_table = """PRAGMA table_info({});""".format(table_name)

        cursor = connection.cursor()
        result = None
        try: 
            cursor.execute(get_whole_table)
            result = cursor.fetchall()
            print(result)
        except Error as e:
            print("The error " + str(e) + " occurred.")


model = Model()
    
