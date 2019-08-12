[![DOI](https://zenodo.org/badge/95352230.svg)](https://zenodo.org/badge/latestdoi/95352230)

# 

## About

Adapted from Django Base Project

## First steps

This project uses modularized settings (to keep sensitive information out of version control or to be able to use the same code for development and production). Therefore you'll have to append a `--settings` parameter pointing to the settings file you'd like to run the code with to all `manage.py` commands.

For development just append `--settings=tieromina.settings.dev` to the following commands, e.g.

1. `python manage.py makemigrations --settings=tieromina.settings.dev`
2. `python manage.py migrate --settings=tieromina.settings.dev`
3. `python manage.py runserver --settings=tieromina.settings.dev`

6. Check [http://127.0.0.1:8000/](http://127.0.0.1:8000/)


## Tests

Install required packages

    pip install -r requirements_test.txt

Run tests

    python manage.py test --settings=tieromina.settings.test
    python manage.py test  --settings=tieromina.settings.dev xl2tei

After running the test a HTML coverage report will be available at cover/index.html


## Jupyter notebook

Check Django baseproject
This [SO link](https://stackoverflow.com/questions/35483328/how-do-i-set-up-jupyter-ipython-notebook-for-django)