import json

from numpy.core.fromnumeric import product

def get_total_from_query(query):
    total_brut = 0
    total_net = 0
    for data in query:
        total_brut += data.amount_brut
        total_net += data.amount_net

    return {
        'total_brut': total_brut,
        'total_net': total_net,
    }


def get_stats_from_query(query):
    result = {
        'nb_repas': 0,
        'nb_cafe': 0,
        'nb_cookie': 0,
        'nb_jus': 0,
        'nb_transactions': 0,
        'total_brut': 0,
        'total_net': 0,
        'categories': {},
    }
    tot = get_total_from_query(query=query)
    result['total_brut'] += tot['total_brut']
    result['total_net'] += tot['total_net']
    for q in query:
        result['nb_transactions'] += 1
        product = json.loads(q.products)
        for k in product.keys():
            if 'repas' in k:
                result['nb_repas'] += product[k]
            if 'cafe' in k:
                result['nb_cafe'] += product[k]
            if 'cookie' in k:
                result['nb_cookie'] += product[k]
            if 'jus' in k:
                result['nb_jus'] += product[k]
            if k not in result['categories']:
                result['categories'][k] = 0
            result['categories'][k] += product[k]
        
    return result