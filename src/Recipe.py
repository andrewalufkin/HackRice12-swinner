import random
import math

class Recipe:
    def __init__(self, genre="mexican", ingredients={"bananas":2}, time=30, cost=20, rating=4.4, reviews=1000):
        self.genre = genre
        self.ingredients = ingredients
        self.time = time
        self.cost = cost
        self.rating = rating
        self.reviews = reviews
    
    def generate_recipe(self):
        """
        Parameters
        ----------
        None.
    
        Returns
        -------
        recipe : Recipe, randomy generated.
        
        This function is used for testing purposes only.
        """
        
        all_genres = ["mexican", "indian", "spanish", "italian", "french", "casual american", "eastern european", "thai", "chinese", "japanese", "korean"]
        all_ingredients = ["bananas", "apples", "carrots", "celery", "chicken breast", "caesar dressing", "yogurt", "butter", "milk", "soy sauce", "peppers", "onion", "cilantro", "porkbutt", "brisket"]
        
        ingredients = {}
        for ingredient in range(5):
            ingredients[random.choice(all_ingredients)] = random.randint(1,5)
        return Recipe(random.choice(all_genres), ingredients, random.randint(20, 60), random.randint(10, 30), \
        round(random.random()*5, 2), random.randint(1,3000))
    
    def generate_recipes(self, num_recipes):
        """
        Parameters
        ----------
        num_recipes : int, the number of recipes we want to generate.
    
        Returns
        -------
        all_recipes : list, all the randomly generated recipes, for arbitrary values.
        
        This function is used for testing purposes only.
        """
            
        all_recipes = []
        for i in range(num_recipes):
            recipe = Recipe()
            recipe = recipe.generate_recipe()
            all_recipes.append(recipe)
        return all_recipes
    
    def optimize_recipes(self, all_recipes, genres=["mexican", "indian", "spanish"], \
    allergies=["bananas", "apples", "carrots"], max_time=60, max_cost=30, min_rating=3, min_reviews=5, n=10):
        """
        Parameters
        ----------
        all_recipes : list, all the recipes that were parsed.
        genre : list, the genre of cuisines that the user likes.
        allergies : list, the allergies or dietary specifications that the user has.
        max_time : int, the max amount of time that the user has / meal.
        max_cost : float, the max cost that a user specified / meal.
        min_rating : float, the min rating out of 5.
        min_reviews : int, the min amount of reviews.
        n : int, the amount of recipes we want to keep
    
        Returns
        -------
        recipes : list, the best n recipes, organized from the greatest to the least rating metric.
        
        We calculate the rating metric by mapping the number of reviews to the natural logarithm function.
        Then, we multiply this value by the rating.
        
        This function is used to filter the best feasible recipes from a large list of recipes.
        """    
        recipes = []
        for recipe in all_recipes:
            if recipe.genre in genres and recipe.ingredients.keys() not in allergies \
            and recipe.time <= max_time and recipe.cost <= max_cost \
            and recipe.rating >= min_rating and recipe.reviews >= min_reviews:
                rating_metric = recipe.rating * math.log(math.e, recipe.reviews)
                if len(recipes) == 0:
                    recipes.append((recipe, rating_metric))
                else:
                    recipe_candidate = 0
                    for i in range(len(recipes)):
                        recipe_candidate = i
                        if recipes[i][1] < rating_metric:
                            break
                    recipes.insert(recipe_candidate, (recipe, rating_metric))
                if len(recipes) > 10:
                    recipes.pop()
        for i in range(len(recipes)):
            recipes[i] = recipes[i][0]
        return recipes