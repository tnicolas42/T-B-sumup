from peewee import CharField, TextField
from app.models import BaseModel
from peewee import CharField
from playhouse.shortcuts import model_to_dict
from app.utils.utils import get_simple_string

ALLERGENE_LIST = [
    get_simple_string("Gluten"),
    get_simple_string("Oeufs"),
    get_simple_string("Lactose"),
    get_simple_string("Fruits à coque"),
    get_simple_string("Arachides"),
    get_simple_string("Moutarde"),
    get_simple_string("Soja"),
    get_simple_string("Sulfites"),
    get_simple_string("Sésame"),
    get_simple_string("Poissons"),
    get_simple_string("Crustacés"),
    get_simple_string("Mollusques"),
    get_simple_string("Céleri"),
    get_simple_string("Lupins"),
]

class Recipe(BaseModel):
    name = CharField()  # name of the recipe
    file_id = CharField()  # id of the recipe file
    img_id = CharField()  # google drive link to image
    img_path = CharField()  # image path

    # search parameters
    search_name = CharField()
    search_ingredients = TextField()
    search_etapes = TextField()
    search_allergene = TextField()

    def to_dict(self, exclude=None, include=None):
        """
        This base method is made to be overridden when you need something removed to added to the returned dictionary
        """
        if include is None:
            include = {}
        if exclude is None:
            exclude = []
        returned_dict = model_to_dict(self)
        for i in exclude:
            returned_dict.pop(i)
        for key, value in include.items():
            returned_dict[key] = value
        return returned_dict