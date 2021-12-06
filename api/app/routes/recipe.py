from flask import Blueprint
from flask import send_file, request
from flask_cors import CORS

from app import gsheet
from app.models.recipe import ALLERGENE_LIST, RECIPE_CATEGORIE, Recipe
from app.utils.recipe import recipe_fetch, recipe_search
from app.utils.recipe import R

recipe_bp = Blueprint("recipe", __name__)
CORS(recipe_bp)

@recipe_bp.route("/recipe/download/<file_id>/<nb>")
def download_recipe(file_id, nb):
    """
    Update the recipe with the right number of people and download it.
    curl --get "http://127.0.0.1:5000/recipe/download/<file_id>/<nb>
    curl --get "http://127.0.0.1:5000/recipe/download/1ZRQtumM4RETSOQUSOoCnGGDKtAZVVC1zv2y0eA2LFY4/4

    Parameters:
        file_id (str): The file id (string in file link).
        nb (int): The number of people desired.

    Returns:
        str: The download url
    """
    gsheet.update_value(cell=R.NB_PERSONNES, value=nb, file_id=file_id, sheet_name=R.SHT_NAME.RECETTE)

    url = "https://docs.google.com/spreadsheets/d/" + file_id + "/export" + \
        "?format=pdf" + \
        "&size=7" + \
        "&portrait=true" + \
        "&gridlines=false" + \
        "&gid=1169815886"
    
    return url, 200


@recipe_bp.route("/recipe/reset")
def recipe_reset():
    """
    Remove all recipe from database
    """
    Recipe.delete().execute()
    return "OK", 200


@recipe_bp.route("/recipe/fetch")
def recipe_fetch_route():
    """
    Fetch all new recipes
    """
    only_new = request.args.get("only_new", False)
    print("Fectching food truck recipes")
    return_1 = recipe_fetch(R.LINK.RECIPES_FOLDER_ID, RECIPE_CATEGORIE.FOOD_TRUCK, only_new=only_new)
    print("Fectching simple recipes")
    return_2 = recipe_fetch(R.LINK.RECIPES_OTHER_FOLDER_ID, RECIPE_CATEGORIE.AUTRES, only_new=only_new)
    if not return_1 or not return_2:
        return "ERROR", 500
    return "OK", 200


@recipe_bp.route("/recipe/list")
def recipe_list():
    """
    Get the list of recipes

    Parameters:
        ?search=... (str): The words to search.
        ?only_name=true/false (bool): Search only on name or in content
        ?categorie=... (str): Search only on a categorie ('All' for all categories)

    Returns:
        list(dict): A list of all recipe and id (eg. [{name: "<nom>", "id": "<id>"}])
    """
    query = None
    search = request.args.get("search", None)
    only_name = request.args.get("only_name", False, type=lambda v: v.lower() == 'true')
    categorie = request.args.get("categorie", 'All')
    allergenic = request.args.get("allergenic", '')
    if allergenic == '':
        allergenic = []
    else:
        allergenic = allergenic.split('.')
    query = recipe_search(
        search=search,
        only_name=only_name,
        categorie=categorie,
        allergenic=allergenic)
    recipes = []
    for q in query:
        recipes.append({
            'id': q.file_id,
            'name': q.name,
            'allergene': q.allergene
        })
    return { 'data': recipes }, 200


@recipe_bp.route("/recipe/image/<file_id>")
def recipe_get_image(file_id):
    query = Recipe.select().where(Recipe.file_id == file_id)
    for q in query:
        path = '../../' + q.img_path
        break
    return send_file(path_or_file=path, mimetype='image/gif')

@recipe_bp.route("/recipe/allergenic_list")
def get_allergenic_list():
    return { 'data': ALLERGENE_LIST }

@recipe_bp.route("/recipe/categorie_list")
def get_categorie_list():
    return { 'data': RECIPE_CATEGORIE.cat_list }