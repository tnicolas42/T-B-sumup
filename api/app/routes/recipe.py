from posixpath import join
from flask import Blueprint
from flask import send_file, request
from flask_cors import CORS
from peewee import fn

from app import gsheet, RUNNING_PORT
from app.models.recipe import Recipe
from app.utils.utils import get_simple_string

class RecipeInfo:
    NB_PERSONNES    = "H9"
    IMG_LINK        = "D4"
    INGREDIENT      = "C9"
    ETAPES          = "C13"
    class SheetName:
        RECETTE     = "Recette"
        FINAL       = "Recette finale"
    SHT_NAME = SheetName()
    class Link:
        RECIPES_FOLDER_ID = "1xZzpaRoEBS8Tetvb-fFGowtuKNqv8E8d"
    LINK = Link()

R = RecipeInfo()

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
def recipe_fetch():
    """
    Fetch all new recipes
    """
    items = gsheet.list_files(R.LINK.RECIPES_FOLDER_ID)
    for i, it in enumerate(items):
        if it['mimeType'] == 'application/vnd.google-apps.spreadsheet':
            print("[%3d%%] %s" % (int(float(i) / len(items) * 100), it['name']))
            recipe = None
            query = Recipe.select().where(Recipe.file_id == it['id'])
            for q in query:
                recipe = q
                break
            if not recipe:  # if recipe already exist
                recipe = Recipe.create(
                    name="",
                    file_id=it['id'],
                    img_id="",
                    img_path="",
                    search_name="",
                    search_ingredients="",
                    search_etapes="",
                )
            recipe.name = it['name']
            recipe.search_name = get_simple_string(it['name'])
            content = gsheet.batch_get_cell(
                cells=[R.INGREDIENT, R.ETAPES],
                file_id=it['id'],
                sheet_name=R.SHT_NAME.FINAL)
            recipe.search_ingredients = get_simple_string(content[0])
            recipe.search_etapes = get_simple_string(content[1])
            img_id = gsheet.get_cell(cell=R.IMG_LINK, file_id=it['id'], sheet_name=R.SHT_NAME.RECETTE)
            if recipe.img_id != img_id:
                img_path = 'assets/recipes/' + it['id'] + '.png'
                gsheet.download_file(file_id=img_id, dest='../' + img_path)
                recipe.img_id = img_id
                recipe.img_path = img_path
            recipe.save()
    print("[100%] Done !")
    return "OK", 200

from peewee import JOIN
@recipe_bp.route("/recipe/list")
def recipe_list():
    """
    Get the list of recipes

    Parameters:
        ?search=... (str): The words to search.
        ?only_name=true/false (bool): Search only on name or in content

    Returns:
        list(dict): A list of all recipe and id (eg. [{name: "<nom>", "id": "<id>"}])
    """
    query = None
    search = request.args.get("search", None)
    only_name = request.args.get("only_name", False, type=lambda v: v.lower() == 'true')
    if search is not None:
        search = get_simple_string(search)
        if only_name:
            query = Recipe.select().where(
                Recipe.search_name.contains(search)
                ).order_by(Recipe.name)
        else:
            query = Recipe.select().where(
                Recipe.search_name.contains(search) |
                Recipe.search_ingredients.contains(search) |
                Recipe.search_etapes.contains(search)
                ).order_by(Recipe.name)

    if query is None:
        query = Recipe.select().order_by(Recipe.name)
    recipes = []
    for q in query:
        recipes.append({
            'id': q.file_id,
            'name': q.name,
        })
    return { 'data': recipes }, 200


@recipe_bp.route("/recipe/image/<file_id>")
def recipe_get_image(file_id):
    query = Recipe.select().where(Recipe.file_id == file_id)
    for q in query:
        path = '../../' + q.img_path
        break
    return send_file(path_or_file=path, mimetype='image/gif')