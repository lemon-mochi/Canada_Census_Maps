import zipfile
import pandas as pd

with zipfile.ZipFile('./census_data/98-401-X2016044_eng_CSV.zip') as z:
    for file in z.namelist():

        if not file.endswith('.csv'):
            continue

        with z.open(file) as f:
            i = 0

            for chunk in pd.read_csv(
                f,
                encoding='latin1',
                low_memory=False,
                chunksize=100_000
            ):

                print(chunk.columns)