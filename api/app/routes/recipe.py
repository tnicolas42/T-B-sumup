from flask import Blueprint
from flask import send_file, request
from flask_cors import CORS

from app import gsheet

class Recipe:
    NB_PERSONNES    = "H9"
    IMG_LINK        = "D4"
    class SheetName:
        RECETTE     = "Recette"
        FINAL       = "Recette finale"
    SHT_NAME = SheetName()
    class Link:
        RECIPES_FOLDER_ID = "1xZzpaRoEBS8Tetvb-fFGowtuKNqv8E8d"
    LINK = Link()

R = Recipe()

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


@recipe_bp.route("/recipe/list")
def recipe_list():
    """
    Get the list of recipes

    Parameters:

    Returns:
        list(dict): A list of all recipe and id (eg. [{name: "<nom>", "id": "<id>"}])
    """
    items = gsheet.list_files(R.LINK.RECIPES_FOLDER_ID)
    recipes = []
    for it in items:
        if it['mimeType'] == 'application/vnd.google-apps.spreadsheet':
            recipes.append({
                'id': it['id'],
                'name': it['name'],
            })
    return { 'data': recipes }, 200


@recipe_bp.route("/recipe/list_with_image")
def recipe_list_with_image():
    """
    Get the list of recipes with coresponding images

    Parameters:

    Returns:
        list(dict): A list of all recipe and id (eg. [{name: "<nom>", "id": "<id>", "img": "<img>"}])
    """
    items = gsheet.list_files(R.LINK.RECIPES_FOLDER_ID)
    recipes = []
    for it in items:
        if it['mimeType'] == 'application/vnd.google-apps.spreadsheet':
            # img = gsheet.get_cell(cell=R.IMG_LINK, file_id=it['id'], sheet_name=R.SHT_NAME.RECETTE)
            # img_path = "assets/recipes/Tranches de potimarron croustillantes et crème aigre.png"
            recipes.append({
                'id': it['id'],
                'name': it['name'],
                'img_url': 'http://127.0.0.1:5001/recipe/image/?name=Tranches de potimarron croustillantes et crème aigre.png',
            })
    return { 'data': recipes }, 200

@recipe_bp.route("/recipe/image/")
def recipe_get_image():
    name = request.args.get("name")
    return send_file(path_or_file='../../assets/recipes/' + name, mimetype='image/gif')