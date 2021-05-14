import logging

import pandas as pd

from omens.models import Witness


class Importer:
    """
    A generic class to import xlsx files into the database
    """

    expected_columns: str = []
    missing_columns: str = []

    def __init__(self, file_to_import):
        self.df = pd.read_excel(file_to_import).fillna("")
        self.validate_header()

    def validate_header(self):
        # df.rename(columns={'oldName1': 'newName1', 'oldName2': 'newName2'}, inplace=True)
        self.missing_columns = []
        for col in self.expected_columns:
            if col not in self.df.columns:
                col_found = False
                for header_col in self.df.columns:
                    if header_col.strip().lower() == col.lower():
                        col_found = True
                        df.rename(columns={header_col: col}, inplace=True)
                        continue

                    else:
                        pass
                if not col_found:
                    self.missing_columns.append(col)
                    logging.warning("Could not find %s", col)

    def read_rows(self):
        for i, row in self.df.iterrows():
            yield row.to_dict()


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

    def save_index(self):
        for row in self.read_rows():
            wit = Witness(
                witness_id=row.get("Siglum"),
                museum_numbers=row.get("Museum numbers"),
                provenance=row.get("provenance"),
                script=row.get("provenance"),
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
                print(repr(e))

        return
