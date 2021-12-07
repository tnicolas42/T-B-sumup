import json
import traceback

from app import gsheet
from app.utils.utils import get_simple_string
from app.models.recipe import Recipe, SIMPLE_ALLERGENE_LIST

class RecipeInfo:
    NB_PERSONNES        = "H9"
    IMG_LINK            = "D4"
    INGREDIENT          = "C9"
    ETAPES              = "C13"
    ALLERGENE           = "D5"
    DEFAULT_IMAGE_ID    = "1MJDNyVt1R_O9JdlMjh_PsIb1mwxEQee_"
    class SheetName:
        RECETTE         = "Recette"
        FINAL           = "Recette finale"
    SHT_NAME = SheetName()
    class Link:
        RECIPES_FOLDER_ID       = "1xZzpaRoEBS8Tetvb-fFGowtuKNqv8E8d"
        RECIPES_OTHER_FOLDER_ID = "1R32AQY90iG5ydZMXKG4iFc0FlSBm2wzS"
    LINK = Link()

R = RecipeInfo()

def recipe_search(search=None, only_name=False, categorie='All', allergenic=[]):
    """
    Search for words in recipe

    Parameters:
        search (str): Search only for recipes with all words in search
        only_name (bool): If true, search only on recipe name, not in content

    Returns:
        peewee.ModelSelect: The query with the result
    """
    query = Recipe.select()
    if categorie != 'All':
        query = query.where(Recipe.categorie == categorie)
    if len(allergenic) > 0:
        for al in allergenic:
            query = query.where(~Recipe.allergene.contains(al))
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

    query = query.order_by(-Recipe.categorie, +Recipe.name)
    
    return query

def recipe_fetch(folder_id, categorie, only_new=True):
    return_success = True
    try:
        items = gsheet.list_files(folder_id)
    except Exception:
        traceback.print_exc()
        return False
    for i, it in enumerate(items):
        if it['mimeType'] == 'application/vnd.google-apps.spreadsheet':
            print("[%s][%3d%%] %s" % (categorie, int(float(i) / len(items) * 100), it['name']))
            recipe = None
            query = Recipe.select().where(Recipe.file_id == it['id'])
            is_new_recipe = True
            for q in query:
                is_new_recipe = False
                recipe = q
                break
            try:
                if not is_new_recipe:  # if recipe already exist
                    if only_new:
                        continue
                else:  # if recipe doesn't exist, create it
                    recipe = Recipe.create(
                        name="",
                        file_id=it['id'],
                        img_id="",
                        img_path="",
                        allergene="",
                        categorie=categorie,
                        search_name="",
                        search_ingredients="",
                        search_etapes="",
                        search_allergene="",
                    )
                recipe.name = it['name']
                recipe.search_name = get_simple_string(it['name'])
                content = gsheet.batch_get_cell(
                    cells=[R.INGREDIENT, R.ETAPES],
                    file_id=it['id'],
                    sheet_name=R.SHT_NAME.FINAL)
                recipe.search_ingredients = get_simple_string(content[0])
                recipe.search_etapes = get_simple_string(content[1])
                allergene = gsheet.get_cell(
                    cell=R.ALLERGENE,
                    file_id=it['id'],
                    sheet_name=R.SHT_NAME.RECETTE)
                recipe.allergene = allergene
                allergene = [al.strip() for al in get_simple_string(allergene).split(',')]
                for al in allergene:
                    if al not in SIMPLE_ALLERGENE_LIST:
                        print("INVALID ALLERGENE: " + al + "(in " + it['name'] + ")")
                recipe.search_allergene = json.dumps(str(allergene))
                img_id = gsheet.get_cell(cell=R.IMG_LINK, file_id=it['id'], sheet_name=R.SHT_NAME.RECETTE)
                if img_id == "":
                    img_id = R.DEFAULT_IMAGE_ID
                if recipe.img_id != img_id:
                    img_path = 'assets/recipes/' + it['id'] + '.png'
                    gsheet.download_file(file_id=img_id, dest='../' + img_path)
                    recipe.img_id = img_id
                    recipe.img_path = img_path
                recipe.save()
            except Exception:
                if is_new_recipe:
                    recipe.delete_instance()
                traceback.print_exc()
                return_success = False
    print("[%s][100%%] Done !" % (categorie))
    return return_success