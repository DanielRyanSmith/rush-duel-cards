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

Deploy
# TODO
gcloud storage rsync ./cardsearch/static/cardsearch gs://ornate-crossbar-465019-c3/static --recursive