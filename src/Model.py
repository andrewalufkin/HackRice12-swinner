from os import curdir
import sqlite3
from sqlite3 import Error
from recipebook.sites.allrecipes import AllRecipes

class Model():

    def __init__(self):
        recipe = AllRecipes("https://www.allrecipes.com/recipe/7004/raisin-brown-bread/")
        print("Image URL:")
        print(recipe.getImage)


    def create_connection(self, path):
        connection = None

        try:
            connection = sqlite3.connect(path)
        except Error as e:
            print("Error " + e + " with connecting to path.")

        return connection

    def execute_query(self, connection, query):
        cursor = connection.cursor()

        if len(query) == 1:
            try:
                cursor.execute(query[0])
                connection.commit()

            except Error as e:
                print("Error " + str(e) + " occurred when executing query.")
        else:
            try:
                cursor.execute(query[0], query[1])
                connection.commit()
            except Error as e:
                print("Error " + str(e) + " occurred when executing query.")

    def initiate_tables(self, connection):
        self.execute_query(connection, [self.create_users_table])
        self.execute_query(connection, [self.create_user_cuisine_table])
        self.execute_query(connection, [self.create_user_ingredients_table])
        self.execute_query(connection, [self.create_recipes_table])
        self.execute_query(connection, [self.recipes_ingredients_table])

    def drop_tables(self, connection):
        self.execute_query(connection, ["""DROP TABLE users"""])
        self.execute_query(connection, ["""DROP TABLE user_cuisine"""])
        self.execute_query(connection, ["""DROP TABLE user_ingredients"""])
        self.execute_query(connection, ["""DROP TABLE recipes"""])
        self.execute_query(connection, ["""DROP TABLE recipe_ingredients"""])

    #Represent the users as a table where each id corresponds to a user. Hold username, password, and time and budget preferences.    
    create_users_table = """CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,

        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL, 

        time INTEGER,
        budget INTEGER

    );"""

    #Represent each users' taste in cuisine. Each column represents a different type of cuisine. A 1 corresponding to the user id
    #of a specific user means that that user enjoys that cuisine, while a 0 means they do not.
    create_user_cuisine_table = """CREATE TABLE IF NOT EXISTS user_cuisine (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cuisine_name INTEGER DEFAULT 0,
        cuisine_name_2 INTEGER DEFAULT 0,
        cuisine_name_3 INTEGER DEFAULT 0
    );"""

    #Represent each users' dietary restrictions. Each column represents a different ingredient. A 1 corresponding to the user id
    #of a specific user means that user can't eat that ingredient, while a 0 means they can.
    create_user_ingredients_table = """CREATE TABLE IF NOT EXISTS user_ingredients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ingredient_name INTEGER,
        ingredient_name_2 INTEGER,
        ingredient_name_3 INTEGER
    );"""
    
    #Represent each recipe by maintaining the time and cuisine type of each recipe.
    create_recipes_table = """CREATE TABLE IF NOT EXISTS recipes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        rating DOUBLE, 
        time INTEGER,
        cuisine TEXT NOT NULL
    );"""

    #Represent each recipe's ingredient list. Each column is a different ingredient, and entries are quantities corresponding to
    #recipe ids.
    recipes_ingredients_table = """CREATE TABLE IF NOT EXISTS recipes_ingredients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ingredient_name TEXT NOT NULL,
        ingredient_name_2 TEXT NOT NULL,
        ingredient_nume_3 TEXT NOT NULL,
    );"""

    cuisine_list = ["cuisine_name", "cuisine_name_2", "cuisine_name_3"]

    ingredient_list = ["ingredient_name", "ingredient_name_2", "ingredient_name_3"]

    def add_user(self, connection, username, password, cuisine, dietary_restrictions, time, budget):

        cur = connection.cursor()
        find_id = None

        add_user = """INSERT INTO users (username, password, time, budget) VALUES(?, ?, ?, ?)"""

        args = (username, password, time, budget)

        query = [add_user, args]

        self.execute_query(connection, query)

        #existing_cuisines = """SELECT * FROM user_cuisine
        #"""

        find_id = """SELECT id FROM users WHERE username = (?)"""

        try:
            cur.execute(find_id, (username, ))
            id = cur.fetchone()[0]
            #Finding id works correctly.
        except Error as e:
            print("The error " + str(e) + " occurred.")

        add_cuisines = """
        INSERT INTO
            'user_cuisine' ('cuisine_name', 'cuisine_name_2', 'cuisine_name_3')
        VALUES
            (?, ?, ?)
        """
        #Note: one question mark is required for each cuisine in cuisine list.

        args = [0 for x in range(len(self.cuisine_list))]
            
        for cuisine_index in range(len(self.cuisine_list)):
            if(self.cuisine_list[cuisine_index] in cuisine):
                
                args[cuisine_index] = 1

        self.execute_query(connection, [add_cuisines, (tuple(args))])

        add_restrictions = """
        INSERT INTO
            'user_ingredients' ('ingredient_name', 'ingredient_name_2', 'ingredient_name_3')
        VALUES
            (?, ?, ?)
        """
        #Note: one question mark is required for each ingredient in ingredient list.

        args = [0 for x in range(len(self.ingredient_list))]

        for ingredient_index in range(len(self.ingredient_list)):
            if(self.ingredient_list[ingredient_index] in dietary_restrictions):

                args[ingredient_index] = 1
                
        self.execute_query(connection, [add_restrictions, (tuple(args))])

    def delete_user(self, connection, username):
        cur = connection.cursor()
        id_to_delete = None

        find_id = """SELECT id FROM users WHERE username = (?)"""

        try:
            cur.execute(find_id, (username, ))
            id_to_delete = cur.fetchone()[0]
            
        except Error as e:
            print("The error " + str(e) + " occurred.")

        delete = """DELETE FROM users WHERE id = (?)"""
        self.execute_query(connection, [delete, (id_to_delete, )])

        delete2 = """DELETE FROM user_cuisine WHERE id = (?)"""
        self.execute_query(connection, [delete2, (id_to_delete, )])

        delete3 = """DELETE FROM user_ingredients WHERE id = (?)"""
        self.execute_query(connection, [delete3, (id_to_delete, )])

        #delete_cuisine = """DELETE FROM user_cuisine WHERE uid = 1"""

        #self.execute_query(connection, [delete_cuisine])

        #delete_ingredients = """DELETE FROM user_ingredients
        #WHERE id = (?)"""

        #self.execute_query(connection, [delete_cuisine, id])
        #self.execute_query(connection, [delete_ingredients, id])

    def print_table(self, connection, table_name):
        
        get_table_info = """PRAGMA table_info({});""".format(table_name)
        get_table_records = "SELECT * from {}".format(table_name)

        cursor = connection.cursor()
        result = None
        try: 
            cursor.execute(get_table_info)
            result = cursor.fetchall()
            print(result)

            cursor.execute(get_table_records)
            result = cursor.fetchall()
            for user in result:
                print(user)
        except Error as e:
            print("The error " + str(e) + " occurred.")
    
    def add_recipe(self, connection, rating, time, cuisine, ingredients):
        
        insert_recipe = """
        INSERT INTO
            'recipes' ('rating', 'time', 'cuisine')
        VALUES
            (?, ?, ?)
        """
        
        args = (rating, time, cuisine)

        self.execute_query(connection, [insert_recipe, args])

        add_ingredients = """
        INSERT INTO
            'recipes_ingredients'
        VALUES
            (?, ?, ?)
        """
        #Note: one question mark is required for each ingredient in ingredient list.

        args = [0 for x in range(len(self.ingredient_list))]

        for ingredient_index in range(len(self.ingredient_list)):
            if(self.ingredient_list[ingredient_index] in ingredients):
                args[ingredient_index] = 1
        
        self.execute_query(connection, [add_ingredients, tuple(args)])


model = Model()
    
