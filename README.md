### Running the search app locally

Setup:
```sh
python -m venv rdc-env; source rdc-env/bin/activate; pip install -r requirements.txt
```

Set up DB:
```sh
python manage.py makemigrations cardsearch; python manage.py migrate --run-syncdb
```

Populate DB:
```sh
# If cards have been previously imported
python manage.py flush
```

```sh
python manage.py runscript add_cards
```

Run the app:
```sh
python manage.py runserver
```

### Searching
Add your search options to the query string. Check `cardsearch/views.py`
to see what you can add to the query. `q=` searches for case-insensitive substring
values.

Examples:
`http://localhost:8000/?attribute=light&mtype=dragon&level=8`
All Level 8 LIGHT Attribute Dragon type monsters.

`http://localhost:800/?ctype=spell&q=draw+1+card`
All spells that mention "draw 1 card" in the text.
