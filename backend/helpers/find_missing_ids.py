
"""
find_missing_ids.py

Find characteristic IDs that exist in {year}_characteristics.csv
but are missing from each column in {year}_{xml/csv}_id_mappings.{xml/csv}.
"""

import pandas as pd


def foo(MAPPINGS_FILE):

    mappings = pd.read_csv(MAPPINGS_FILE, dtype=str)

    # Valid target IDs from the first column of the characteristics file.
    valid_ids = set(mappings["Characteristic_ID"].dropna().str.strip())

    # The first column contains the IDs to print.
    target_ids = mappings.iloc[:, 0].str.strip()

    for column in mappings.columns[1:]:
        # IDs in this XML column that are present in the characteristics file.
        mapped_ids = set(mappings[column].dropna().str.strip()) & valid_ids

        # Print first-column IDs whose corresponding XML mapping is missing.
        missing = mappings.loc[
            mappings[column].isna()
            | mappings[column].str.strip().eq(""),
            mappings.columns[0]
        ]

        missing = sorted(
            set(missing.dropna().str.strip()) & valid_ids,
            key=int
        )

        print(f"\n{column}:")
        print(missing)


MAPPINGS_FILE = "../mappings/xml_mappings/2006_xml_id_mappings.csv"
foo(MAPPINGS_FILE)
MAPPINGS_FILE = "../mappings/xml_mappings/2001_xml_id_mappings.csv"
foo(MAPPINGS_FILE)
MAPPINGS_FILE = "../mappings/xml_mappings/1996_xml_id_mappings.csv"
foo(MAPPINGS_FILE)
MAPPINGS_FILE = "../mappings/csv_mappings/1991_csv_id_mappings.csv"
foo(MAPPINGS_FILE)
MAPPINGS_FILE = "../mappings/csv_mappings/1986_csv_id_mappings.csv"
foo(MAPPINGS_FILE)
MAPPINGS_FILE = "../mappings/csv_mappings/1981_csv_id_mappings.csv"
foo(MAPPINGS_FILE)


