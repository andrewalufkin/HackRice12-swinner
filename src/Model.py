from os import curdir
import sqlite3
from sqlite3 import Error
from bs4 import BeautifulSoup
import requests
import json
import os

class Model():

    def __init__(self):

        directory = "HackRice12-swinner/src/demo_recipes"

        connection = self.create_connection("E:\\sm_app.sqlite")

        self.initiate_tables(connection)

        print("Before")
        self.print_table(connection, "recipes")

        for filename in os.listdir(directory):
            f = os.path.join(directory, filename)

            if os.path.isfile(f):
                #self.add_recipe(connection, f)
                pass
        

        print("After")
        self.print_table(connection, "recipes")
        

       
        
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
        self.execute_query(connection, [self.create_recipes_table])

    def drop_tables(self, connection):
        self.execute_query(connection, ["""DROP TABLE users"""])
        self.execute_query(connection, ["""DROP TABLE recipes"""])

    #Represent the users as a table where each id corresponds to a user. Hold username, password, and time and budget preferences.    
    create_users_table = """CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,

        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL, 

        time INTEGER,
        budget INTEGER,

        cuisines_jsonpath TEXT NOT NULL,
        ingredients_jsonpath TEXT NOT NULL

    );"""

    #Represent each users' dietary restrictions. Each column represents a different ingredient. A 1 corresponding to the user id
    #of a specific user means that user can't eat that ingredient, while a 0 means they can.
    create_user_ingredients_table = """CREATE TABLE IF NOT EXISTS user_ingredients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ingredients TEXT NOT NULL
    );"""
    
    #Represent each recipe by maintaining the time and cuisine type of each recipe.
    create_recipes_table = """CREATE TABLE IF NOT EXISTS recipes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        jsonpath STRING,
        rating DOUBLE, 
        time STRING
    );"""

    def add_user(self, connection, username, password, cuisine, dietary_restrictions, time, budget):

        cur = connection.cursor()
        find_id = None

        add_user = """INSERT INTO users (username, password, time, budget) VALUES(?, ?, ?, ?)"""

        args = (username, password, time, budget)

        query = [add_user, args]

        self.execute_query(connection, query)

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
    
    def add_recipe(self, connection, jsonpath):
        
        insert_recipe = """
        INSERT INTO
            'recipes' ('jsonpath', 'rating', 'time')
        VALUES
            (?, ?, ?)
        """
        
        f = open(jsonpath, 'r')
        data = json.loads(f.read())

        url = data["url"]
        
        rating = self.get_ratings(url)
        
        time = self.get_time(url)

        print(time)
        
        args = (jsonpath, rating, time)

        self.execute_query(connection, [insert_recipe, args])

    def get_image(jsonpath):
        parser = "lxml"

        f = open(jsonpath, 'r')
        data = json.loads(f.read())

        url = data["url"]
        article_name = data["title"]

        htmldoc = requests.get(url).text
        soup = BeautifulSoup(htmldoc, parser)

        images = soup.findAll('img')
        for image in images:

            if(article_name in str(image)):
                image = image["src"]
                return image

    def get_ratings(self, url):
        parser = "lxml"

        htmldoc = requests.get(url).text
        soup = BeautifulSoup(htmldoc, parser)

        divs = soup.find_all("div", {"class": "component recipe-reviews container-full-width clearfix template-two-col with-sidebar-right hidden"})

        for div in divs:
            return div.get('data-ratings-average')

    def get_time(self, url):
        counter = 0
        parser = "lxml"

        htmldoc = requests.get(url).text
        soup = BeautifulSoup(htmldoc, parser)

        divs = soup.find_all("div", {"class": "recipe-meta-item"})

        for div in divs:
            int_divs = div.findAll("div")
            for int_div in int_divs:

                if counter == 1:
                    return int_div.string 

                if int_div.string == "total:":
                    counter = 1

    def get_ingredients(jsonpath):
        f = open(jsonpath, 'r')
        data = json.loads(f.read())

        return data["ingredients"]
    
    def get_instructions(jsonpath):
        f = open(jsonpath, 'r')
        data = json.loads(f.read())

        return data["directions"]

    def is_valid_allrecipes(jsonpath):
        f = open(jsonpath, 'r')
        data = json.loads(f.read())
        
        return data["source"] == "allrecipes.com"

    

    def generate_cuisine(name):
        name = name.lower()
        if "taco" in name or "quesadilla" in name or "burrito" in name or \
        "mex" in name or 'salsa' in name:
            return "mexican"
        elif 'pasta' in name or 'pizza' in name:
            return 'italian'
        elif 'hummus' in name or 'falafel' in name or 'pita' in name:
            return 'mediterranean'
        elif 'curry' in name or 'masala' in name or 'chaat' in name:
            return 'indian'
        elif 'burger' in name or 'fries' in name or 'pancakes' in name or 'waffles' in name:
            return 'american'
        elif 'chow mein' in name or 'noodles' in name or 'fried rice' in name or \
        'dumpling' in name or 'spring roll' in name:
            return 'chinese'
        elif 'crepes' in name or 'quiche' in name or 'croissant' in name or 'baguette' in name:
            return 'french'
        return None

    
    def generate_allergies(ingredients):
        # ingredients is a list
        allergies = []
        for ingredient in ingredients:
            if ('milk' in ingredient or 'cheese' in ingredient or 'yogurt' in ingredient or \
            'butter' in ingredient) and ('dairy' not in allergies):
                allergies.append('dairy')
            elif ('chicken' in ingredient or 'beef' in ingredient or 'sausage' in ingredient or \
            'bacon' in ingredient or 'fish' in ingredient or 'salmon' in ingredient or 'ham' in ingredient \
            or 'turkey' in ingredient) and ('meat' not in allergies):
                allergies.append('meat')
            elif ('peanut' in ingredient or 'almond' in ingredient or 'cashew' in ingredient or \
            'nut' in ingredient) and ('nuts' not in allergies):
                allergies.append('nuts')
            elif ('egg' in ingredient and 'eggs' not in allergies):
                allergies.append('eggs')
            elif ('lobster' in ingredient or 'crab' in ingredient or 'shrimp' in ingredient or \
            'oyster' in ingredient) and ('shellfish' not in allergies):
                allergies.append('shellfish')
        if len(allergies) > 0:
            return allergies
        else:
            return None

                
               

m = Model()