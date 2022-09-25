import math
from Recipe import Recipe

class Cart:
    def __init__(self, recipes=Recipe(), packages={}, leftovers={}, price=0.0):
        # constructs a new dictionary, s.t. every ingredient maps to its total price
        self.recipes = recipes
        self.packages = packages
        self.leftovers = leftovers
        self.price = price
        
    def create_cart(self, recipes, packages, unit_prices):
        """
        Parameters
        ----------
        recipes : list, all the recipes that were added to cart.
        packages : dict, ingredients from the grocery store : package size.
        unit_prices : dict, packages from the grocery store : their price.

        Returns
        -------
        price : float, the total cost combining all the ingredients, 
        from all the recipes.
        combined_packages : dict, ingredients from the grocery store : number of packages

        We take care to avoid double counting ingredients and take into 
        account leftover ingredients from past purchases
        """
        combined_packages = {}
        leftovers = {}
        price = 0
        for recipe in recipes:
            for ingredient in recipe.ingredients:
                if ingredient in combined_packages:
                    combined_packages[ingredient] += recipe.ingredients[ingredient] / packages[ingredient]
                else:
                    combined_packages[ingredient] = recipe.ingredients[ingredient] / packages[ingredient]
        for ingredient in combined_packages:
            leftovers[ingredient] = math.ceil(combined_packages[ingredient]) - combined_packages[ingredient]
            combined_packages[ingredient] = math.ceil(combined_packages[ingredient])
            price += (combined_packages[ingredient] * unit_prices[ingredient])
            
        return Cart(recipes, combined_packages, leftovers, price)
    
# packages = {"bananas": 2, "apples": 2, "carrots": 2, "celery": 1, "chicken breast": 1, "caesar dressing": 1, "yogurt": 5, "butter": 6, "milk": 4, "soy sauce": 3, "peppers": 3, "onion": 10, "cilantro": 100, "porkbutt": 4, "brisket": 5}
# unit_prices = {"bananas": 5, "apples": 5, "carrots": 3, "celery": 2, "chicken breast": 8, "caesar dressing": 4, "yogurt": 4, "butter": 4, "milk": 4, "soy sauce": 20, "peppers": 5, "onion": 7, "cilantro": 50, "porkbutt": 8, "brisket": 20}
    
# my_recipes = Recipe().generate_recipes(1000)
# my_recipes = Recipe().optimize_recipes(my_recipes)
# cart = Cart()
# cart = Cart().create_cart(my_recipes, packages, unit_prices)