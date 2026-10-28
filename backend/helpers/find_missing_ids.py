
"""
find_missing_ids.py

Find missing characteristic IDs by geographic level.
For 1981-1991, merge Part A and Part B columns belonging
to the same geographic level before checking for missing IDs.
"""

import re
from pathlib import Path

import pandas as pd


MAPPING_DIRS = {
    "xml": Path("../mappings/xml_mappings"),
    "csv": Path("../mappings/csv_mappings"),
}
CHARACTERISTICS_DIR = Path("../characteristics")


def foo(year, mapping_type):
    mappings_file = (
        MAPPING_DIRS[mapping_type]
        / f"{year}_{mapping_type}_id_mappings.csv"
    )
    characteristics_file = (
        CHARACTERISTICS_DIR / f"{year}_characteristics.csv"
    )

    mappings = pd.read_csv(mappings_file, dtype=str)
    characteristics = pd.read_csv(characteristics_file, dtype=str)

    mappings.columns = mappings.columns.str.strip()
    characteristics.columns = characteristics.columns.str.strip()

    id_column = mappings.columns[0]
    mappings[id_column] = mappings[id_column].str.strip()

    characteristics["CHARACTERISTIC_ID"] = (
        characteristics["CHARACTERISTIC_ID"].str.strip()
    )

    valid_ids = set(
        characteristics["CHARACTERISTIC_ID"].dropna()
    )
    names = dict(zip(
        characteristics["CHARACTERISTIC_ID"],
        characteristics["CHARACTERISTIC_NAME"],
    ))

    # Group mapping columns by geographic level, merging Part A/B.
    groups = {}

    for column in mappings.columns[1:]:
        # E.g. 1981_CT_Part_A -> 1981_CT
        #      1981_PR_CD_CSD_Part_B -> 1981_PR_CD_CSD
        level = re.sub(r"_Part_[AB]$", "", column)
        groups.setdefault(level, []).append(column)

    print(f"\n## {year}\n")

    for level, columns in groups.items():
        # A target ID is mapped if ANY Part A/B column has a value.
        combined = mappings[columns].replace(r"^\s*$", pd.NA, regex=True)
        missing_mask = combined.isna().all(axis=1)

        missing = sorted(
            set(mappings.loc[missing_mask, id_column].dropna())
            & valid_ids,
            key=int,
        )

        if not missing:
            continue

        print(f"### Missing for all {level} geographies\n")
        print("| CHARACTERISTIC_ID | CHARACTERISTIC_NAME |")
        print("|---:|---|")

        for characteristic_id in missing:
            name = str(names[characteristic_id]).strip()
            print(f"| {characteristic_id} | {name} |")

        print()


for year in (2006, 2001, 1996):
    foo(year, "xml")

for year in (1991, 1986, 1981):
    foo(year, "csv")
