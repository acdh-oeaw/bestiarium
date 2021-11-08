[![flake8 Lint](https://github.com/acdh-oeaw/bestiarium/actions/workflows/lint.yml/badge.svg)](https://github.com/acdh-oeaw/bestiarium/actions/workflows/lint.yml)

# Bestiarium Mesopotamicum

Code repo for FWF Project [Bestiarium Mesopotamicum: Tieromina im Alten Mesopotamien](https://pf.fwf.ac.at/de/wissenschaft-konkret/project-finder/42881)


## Install

* create a postgres-db
* adapt `settings.py` to match your database
* create a virtual environment and install dependencies `pip install -r requirements.txt`
* make migrations and run migrations
* start the dev server`

1. `python manage.py migrate`
1. `python manage.py runserver`
