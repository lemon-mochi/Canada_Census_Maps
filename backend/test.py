import pandas as pd
import zipfile


zip_path = './census_data/98-316-XWE2011001-101_CSV.zip'

with zipfile.ZipFile(zip_path) as z:
    for file in z.namelist():
        test_path = zip_path[14:-8]
        print(test_path)

        if (file != test_path + ".CSV"):
            continue

        print(f"Processing {file}")

        with z.open(file) as f:
            for chunk in pd.read_csv(
                f,
                encoding='latin1',
                low_memory=False,
                header=0,
                na_values=['x', 'X', '..', 'F', '...', 'null', 'NULL'],
                chunksize=100_00
            ):
                print(chunk.head)