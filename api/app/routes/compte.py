from flask import Blueprint

from app import gsheet, TBCOMPTE

compte_bp = Blueprint("compte", __name__)

@compte_bp.route("/compte/charges", methods=["GET"])
def get_charges():
    total_charges = gsheet.get_cell('M4', **TBCOMPTE.CHARGES)
    return {
        'charges': total_charges,
    }, 200


@compte_bp.route("/compte/produits", methods=["GET"])
def get_produits():
    result = gsheet.batch_get_cell(['L4', 'L7'], **TBCOMPTE.PRODUITS)
    total_produits = result[0]
    recu = result[1]
    return {
        'produits': total_produits,
        'recu': recu,
    }, 200

@compte_bp.route("/compte/test")
def test():
    gsheet.batch_update_cell(['A1', 'C4'], ['a', 'b'], **TBCOMPTE.TEST)
    return "ok", 200