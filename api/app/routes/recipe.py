from flask import Blueprint
from flask import send_file, request
from flask_cors import CORS

from app import gsheet, RUNNING_PORT
from app.models.recipe import Recipe

class RecipeInfo:
    NB_PERSONNES    = "H9"
    IMG_LINK        = "D4"
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


@recipe_bp.route("/recipe/fetch")
def recipe_fetch():
    items = gsheet.list_files(R.LINK.RECIPES_FOLDER_ID)
    Recipe.delete().execute()
    for it in items:
        if it['mimeType'] == 'application/vnd.google-apps.spreadsheet':
            img_link = gsheet.get_cell(cell=R.IMG_LINK, file_id=it['id'], sheet_name=R.SHT_NAME.RECETTE)
            img_path = 'assets/recipes/' + it['id'] + '.png'
            gsheet.download_file(file_id=img_link, dest='../' + img_path)
            Recipe.create(
                name=it['name'],
                file_id=it['id'],
                img_id=img_link,
                img_path=img_path,
            )
    return "OK", 200


@recipe_bp.route("/recipe/list")
def recipe_list():
    """
    Get the list of recipes

    Parameters:

    Returns:
        list(dict): A list of all recipe and id (eg. [{name: "<nom>", "id": "<id>"}])
    """
    recipes = []
    query = Recipe.select()
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