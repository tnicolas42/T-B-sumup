from flask import Blueprint
from flask import redirect

from app import gsheet

recipe_bp = Blueprint("recipe", __name__)

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
    sheet_name = "Recette"
    gsheet.update_value(cell="H8", value=nb, file_id=file_id, sheet_name=sheet_name)

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
    items = gsheet.list_files("1xZzpaRoEBS8Tetvb-fFGowtuKNqv8E8d")
    recipes = []
    for it in items:
        if it['mimeType'] == 'application/vnd.google-apps.spreadsheet':
            recipes.append({
                'id': it['id'],
                'name': it['name'],
            })
    return { 'data': recipes }, 200