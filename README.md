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


## workflow / debug

started with code from commit: https://gitlab.com/acdh-oeaw/bestiarium-mesopotamicum/webapp/-/tree/618e2642ff17e4afd5f3616030ed71082269e10b

(to make the app working on a fresh database you'll need to manually run `python manage.py makemigrations omens` and `python manage.py makemigrations curator`; at some point migration files should be checked in)

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
  * fixing this bug by removing reference to 'row' [commit](https://gitlab.com/acdh-oeaw/bestiarium-mesopotamicum/webapp/-/commit/c08b162b7623715280d591fe0a629c791ab7fb08)
* reupload of omen-file
  * failes due to yet another data-issue, "BM 38313" referenced in data but witness id is BM 038313, changed wrong data in sheet 37.37
* delete everything / reupload everything

```
Ants 37.21-37.40 final.xlsx:
Unrecognised row header; idno: Var. (A 441+) (trl)
Unrecognised row header; idno: Var. (A 441+) (trl)
Unrecognised row header; idno: Var. (A 441+) (trl)
Unrecognised row header; idno: Var. (A 441+) (trl)
```

which looks like some regex issue in the same function with the bug fixed above; `omens/reconstruction.py`

```python
class ReconstructionId(namedtuple("ReconstructionId", "omen_prefix,label,witness")):
    @classmethod
    def idno_parts(cls, idno):
        m = re.match(
            r"^(?P<label>[a-zA-Z\s]*)\s(?P<siglum>.*)\((?P<rdg_type>[a-zA-Z]*)\)$", idno
        )
        if not m:
            raise ValueError(f"Unrecognised row header; idno: {idno}", )
        return namedtuple("idno", "label,witness,rdg_type")(
            label=m.group("label"),
            witness=m.group("siglum")[1:-2],
            rdg_type=m.group("rdg_type"),
        )
```

by rewriting `def idno_parts(cls, idno)` like

```python
if not m:
    # raise ValueError(f"Unrecognised row header; idno: {idno}", )
    return namedtuple("idno", "label,witness,rdg_type")(
        label=idno,
        witness=idno,
        rdg_type='trl',
    )
``` 

the import goes through, next step would be to parse the currently hard_code rdg_type from the actual value

