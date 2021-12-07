# timbastien refactoring

## API
```python
# TODO
interface de connection:
-> creation / connection a un compte utilisateur (admin ou normal)
-> connection a google API (uniquement si utilisateur == admin)
    uniquement 1 fois ?
-> connection a sumup API (uniquement si utilisateur == admin)
    a chaque fois ?
```

```python
/recipes/download/<file_id>/<nb>  # download a recipe for nb peoples
/recipes/reset  # delete all saved recipes
/recipes/fetch  # fetch all new recipes
    ?only_new=<bool>  # fetch only new recipes (otherwise, update all)
/recipes/fetch/<file_id>  # fetch or update only one recipe
/recipes/search  # search for recipes
    ?search=... (str): The words to search.
    ?only_name=true/false (bool): Search only on name or in content
    ?categorie=... (str): Search only on a categorie ('All' for all categories)
/recipes/image/<file_id>  # get the image for a given recipe
/recipes/allergenic_list  # get the list of all allergenic
/recipes/categories_list  # get the list of all categories
```

```python
/transactions/fecth_all  # fetch all new transactions
/transactions/size  # get the number of transactions
/transaction/get/last  # get the last transaction data
/transactions/get_weeks  # get the list of all weeks of the project
/transactions/week/<week>/data  # get data about a week (total, payment type, ...)

/transactions/stats/total  # get total (brut/net) of all transactions
/transactions/stats/get_interval/<start_date>/<end_date>  # get informations about payments, stats, ... in a time interval
```

```python
/comptes/charges  # get total charges of the project
/comptes/products  # get total and received product of the project
```

## Questions
- Comment je gere les connections a google et sumup ?

- Ya moyen de rester connecter a sumup ? ya moy de pas avoir de pbs avec la deconnection au bout d'une heure ?

- comment on fait pour qu'un appel API puisse pas etre paralelisé ? (genre on peut pas avoir 2 fetch en meme temps)

- faut gerer des bail d'acces en meme temps a une database ?

- ya besoin de celeri ?
