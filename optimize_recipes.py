import random
import math

class optimize_recipes:
    def __init__(self, styles, allergies, max_time, max_cost, min_rating, min_reviews):
        self.styles = styles
        self.allergies = allergies
        self.max_time = max_time
        self.max_cost = max_cost
        self.min_rating = min_rating
        self.min_reviews = min_reviews
    
    # populate recipes (a list) with properties (dict) for each recipe
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
        all_styles = ["mexican", "indian", "spanish", "italian", "french", "casual american", "eastern european", "thai", "chinese", "japanese", "korean"]
        all_ingredients = ["bananas", "apples", "carrots", "celery", "chicken breast", "caesar dressing", "yogurt", "butter", "milk", "soy sauce", "peppers", "onion", "cilantro", "porkbutt", "brisket"]
            
        all_recipes = []
        for i in range(num_recipes):
            ingredients = {}
            for j in range(5):
                ingredients[random.choice(all_ingredients)] = random.randint(1,5)
            all_recipes.append({"style" : random.choice(all_styles),
                                "ingredients" : ingredients,
                                "time": random.randint(20, 60),
                                "cost": random.randint(10, 30),
                                "rating": round(random.random()*5, 2),
                                "reviews": random.randint(1,3000)})
            #print(all_recipes[i]["rating"], all_recipes[i]["reviews"])
        return all_recipes
        
    def optimize(self, all_recipes, styles, allergies, max_time, max_cost, min_rating, min_reviews, n):
        """
        Parameters
        ----------
        all_recipes : list, all the recipes that were parsed.
        styles : list, the style of cuisines that the user likes.
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
            if recipe["style"] in styles and recipe["ingredients"].keys() not in allergies \
            and recipe["time"] <= max_time and recipe["cost"] <= max_cost \
            and recipe["rating"] >= min_rating and recipe["reviews"] >= min_reviews:
                rating_metric = recipe["rating"] * math.log(math.e, recipe["reviews"])
                #print(rating_metric)
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
        return recipes