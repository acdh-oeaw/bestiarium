# webapp

A webapp for entering data in the project Bestiarium Mesopotamicum: Animal Omens in Ancient Mesopotamia (OFWF31032)

## install

* clone the repo
* optional: create a virtual-env
* install requirements `pip install -r requirements` (tested on ubuntu v20.x)
* change into the `src` directory
* run the server `python manage.py runserver --settings=tieromina.settings.pg_local`
  * this will most likely fail as you won't have a postgres-db with postgis-extension called `tieromina`, therefore get a recent dump of the production database locally and adapt the `pg_local.py` settings accordingly.
  * try to run `makemigrations` and `migrate` command (not tested)
