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