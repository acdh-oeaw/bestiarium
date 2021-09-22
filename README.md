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


## ToDo

### Bringing GitLab-Repo and code on the server in sync

* currently the production version runs on the branch https://gitlab.com/acdh-oeaw/bestiarium-mesopotamicum/webapp/-/tree/feature/final (which was not checked in the gitlab repo)
* I updated the code from the server locally to django>=3.2 and updated/cleaned the `requirements.txt` accordingly
* merged `feature/final` into `master`
* merged `develop` into `master`


## workflow

* Upload an index-file e.g. https://oeawcloud.oeaw.ac.at/index.php/f/35784358
  * 7 Witnesses: u.a. 'A441 +'
* Upload omen-file e.g. https://oeawcloud.oeaw.ac.at/index.php/f/36945156
  * fails because of 
  
>Ants 37.21-37.40 final.xlsx: Unknown siglum - "A 441+". Unable to find any siglum starting with A 441 for Omen 37.21 in sheet 37.21

-> Either the index file or the omen file is false `A 441+` vs `A441 +`

* delete all chapters, witnesses
* changed in `37.21-37.40 final.xlsx` everywhere `A441 +` into `A 441+`
* reupload of index-file
* reupload of omen-file
  * fails with error (variable 'row' referenced which does not exist, https://gitlab.com/acdh-oeaw/bestiarium-mesopotamicum/webapp/-/blob/master/src/omens/reconstruction.py#L31)
  * fixing this bug by removing reference to 'row'
 
