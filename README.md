[![flake8 Lint](https://github.com/acdh-oeaw/bestiarium/actions/workflows/lint.yml/badge.svg)](https://github.com/acdh-oeaw/bestiarium/actions/workflows/lint.yml)

# Bestiarium Mesopotamicum

Code repo for FWF Project [Bestiarium Mesopotamicum: Tieromina im Alten Mesopotamien](https://pf.fwf.ac.at/de/wissenschaft-konkret/project-finder/42881)


## Install

* create a postgres-db
* adapt `settings.py` to match your database
* create a virtual environment and install dependencies `pip install -r requirements.txt`
* make migrations and run migrations
* start the dev server

1. `python manage.py migrate`
1. `python manage.py runserver`


## Docker

At the ACDH-CH we use a centralized database-server. So instead of spawning a database for each service our services are talking to a database on this centralized db-server. This setup is reflected in the dockerized setting as well, meaning it expects an already existing database (either on your host, e.g. accessible via 'localhost' or some remote one)

### building the image

* `docker build -t bestiarium:latest .`
* `docker build -t bestiarium:latest --no-cache .`


### running the image

To run the image you should provide an `.env` file to pass in needed environment variables; see example below:

* `docker run -it -p 8020:8020 --rm --env-file env.default --name bestiarium bestiarium:latest`