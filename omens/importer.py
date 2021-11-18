import logging

import pandas as pd


class Importer:
    """
    A generic class to import xlsx files into the database
    """

    expected_columns: str = []
    missing_columns: str = []

    def __init__(self, file_to_import, sheet_name=0):
        """
        @file_to_import: name of the excel file
        @sheet_name: str, int, list, or None, default 0
          Strings are used for sheet names.
          Integers are used in zero-indexed sheet positions.
          Lists of strings/integers are used to request multiple sheets.
          Specify None to get all sheets.
          Available cases:
          Defaults to 0: 1st sheet as a DataFrame
          1: 2nd sheet as a DataFrame
          "Sheet1": Load sheet with name “Sheet1”
          [0, 1, "Sheet5"]: Load first, second and sheet named “Sheet5” as a dict of DataFrame
          None: All sheets.
        """
        self.fname = file_to_import._name
        self.df = pd.read_excel(file_to_import, sheet_name=sheet_name).fillna("")
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
                        df.rename(columns={header_col: col}, inplace=True)  # noqa: F821
                        continue

                    else:
                        pass
                if not col_found:
                    self.missing_columns.append(col)
                    logging.warning("Could not find %s", col)

    def read_rows(self):
        for i, row in self.df.iterrows():
            yield {k.strip(): str(v).strip() for k, v in row.to_dict().items()}
