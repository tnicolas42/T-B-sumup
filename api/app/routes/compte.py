from flask import Blueprint
from flask import request
from flask_cors import CORS

from app import gsheet, TBCOMPTE
from app.utils.google_sheets_api import MAJOR_DIMENSION, VALUE_RENDER_OPTION, DATE_TIME_RENDER_OPTION

compte_bp = Blueprint("compte", __name__)
CORS(compte_bp)

@compte_bp.route("/compte/charges", methods=["GET"])
def get_charges():
    """
    Get the total charges of the project
    """
    total_charges = gsheet.get_cell('M4', **TBCOMPTE.CHARGES)
    return {
        'charges': total_charges,
    }, 200


@compte_bp.route("/compte/produits", methods=["GET"])
def get_produits():
    """
    Get the total and received product
    """
    result = gsheet.batch_get_cell(['L4', 'L7'], **TBCOMPTE.PRODUITS)
    total_produits = result[0]
    recu = result[1]
    return {
        'produits': total_produits,
        'recu': recu,
    }, 200


@compte_bp.route("/compte/get/range/<cells>")
def get_range(cells: str):
    """
    Get the selected values range (eg. Produits!C1:J12) 
    curl --get 'http://127.0.0.1:5000/compte/get/range/Produits!C1:H2?value_render_option=UNFORMATTED_VALUE'
    """
    sheet_name, cells = cells.split("!")

    major_dimension = request.args.get('major_dimension')
    if major_dimension is None:
        major_dimension = MAJOR_DIMENSION.DEFAULT
    value_render_option = request.args.get('value_render_option')
    if value_render_option is None:
        value_render_option = VALUE_RENDER_OPTION.DEFAULT
    date_time_render_option = request.args.get('date_time_render_option')
    if date_time_render_option is None:
        date_time_render_option = DATE_TIME_RENDER_OPTION.DEFAULT

    result = gsheet.get_range(
        cells=cells,
        file_id=TBCOMPTE.CHARGES['file_id'],
        sheet_name=sheet_name,
        major_dimension=major_dimension,
        value_render_option=value_render_option,
        date_time_render_option=date_time_render_option)
    return {
        'data': result,
    }, 200


@compte_bp.route("/compte/get/cell/<cell>")
def get_cell(cell: str):
    """
    Get the selected values cell (eg. Produits!C1) 
    curl --get 'http://127.0.0.1:5000/compte/get/cell/Produits!C1?value_render_option=UNFORMATTED_VALUE'
    """
    sheet_name, cell = cell.split("!")

    value_render_option = request.args.get('value_render_option')
    if value_render_option is None:
        value_render_option = VALUE_RENDER_OPTION.DEFAULT
    date_time_render_option = request.args.get('date_time_render_option')
    if date_time_render_option is None:
        date_time_render_option = DATE_TIME_RENDER_OPTION.DEFAULT

    result = gsheet.get_cell(
        cell=cell,
        file_id=TBCOMPTE.CHARGES['file_id'],
        sheet_name=sheet_name,
        value_render_option=value_render_option,
        date_time_render_option=date_time_render_option)
    return {
        'data': result,
    }, 200


@compte_bp.route("/compte/test")
def test():
    gsheet.batch_update_cell(['A1', 'C4'], ['a', 'b'], **TBCOMPTE.TEST)
    return "ok", 200