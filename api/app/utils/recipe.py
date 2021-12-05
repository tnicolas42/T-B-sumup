from flask import request

from app.utils.utils import get_simple_string
from app.models.recipe import Recipe

def recipe_search(search=None, only_name=False):
    """
    Search for words in recipe

    Parameters:
        search (str): Search only for recipes with all words in search
        only_name (bool): If true, search only on recipe name, not in content

    Returns:
        peewee.ModelSelect: The query with the result
    """
    query = Recipe.select()
    if search is not None:
        search = get_simple_string(search)

        for word in search.split():
            if only_name:
                query = query.where(
                    Recipe.search_name.contains(word)
                    )
            else:
                query = query.where(
                    Recipe.search_name.contains(word) |
                    Recipe.search_ingredients.contains(word) |
                    Recipe.search_etapes.contains(word)
                    )

    query = query.order_by(Recipe.name)
    
    return query