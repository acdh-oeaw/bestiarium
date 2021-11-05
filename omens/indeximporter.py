from omens.models import Witness

from .importer import Importer


class IndexImporter(Importer):
    """
    Imports index files into the database
    """

    expected_columns = [
        "Siglum",
        "Museum numbers",
        "Provenance",
        "Script",
        "State of publication",
        "State of preservation",
        "Type of manuscript",
        "šumma ālu Tablets attested",
        "Omens attested",
        "CDLI number",
        "Remarks",
    ]

    def save(self):
        """
        Saves witnesses in Witness model
        """
        for row in self.read_rows():
            if not row.get("Siglum"):
                continue
            wit = Witness(
                witness_id=row.get("Siglum"),
                museum_numbers=row.get("Museum numbers"),
                provenance=row.get("Provenance"),
                script=row.get("Script"),
                state_publication=row.get("State of publication"),
                state_preservation=row.get("State of preservation"),
                manuscript_type=row.get("Type of manuscript"),
                tablets_attested=row.get("šumma ālu Tablets attested"),
                omens_attested=row.get("Omens attested"),
                cdli_number=row.get("CDLI number"),
                remarks=row.get("Remarks"),
            )
            try:
                wit.save()
            except Exception as e:
                return {self.fname: repr(e)}

        return
