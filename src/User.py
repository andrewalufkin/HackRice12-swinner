from collections import defaultdict
#Defines a user class for the project.

class User():
    ingredients = defaultdict(str)

    
    def __init__(self, username, password, cuisine, dietary_restrictions, time, budget):
        """Initializes the User class. Call upon adding a user to the network.

        Args:
            username (string): The username of the user.
            password (password): The user's password.
            cuisine (list): A list of cuisines the user enjoys.
            dietary_restrictions (list): A list of ingredients the user is allergic to
            time (int): The time the user has to prepare meals.
            budget (int): The amount the user can afford to spend on meals.
        """
        self.username = username 
        self.password = password
        self.cuisine = cuisine
        self.dietary_restrictions = dietary_restrictions
        self.time = time
        self.budget = budget

    def add_ingredient(self, ingredient, quantity):
        self.ingredients[ingredient] += quantity

    def subtract_ingredient(self, ingredient, quantity):
        self.ingredients[ingredient] -= quantity

    




