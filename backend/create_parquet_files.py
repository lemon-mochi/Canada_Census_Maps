import pandas as pd
import numpy as np
import zipfile
import os
import pyarrow as pa
import pyarrow.parquet as pq

os.makedirs("parquet_data", exist_ok=True)

cols = [
    'CENSUS_YEAR',
    'DGUID',
    'GEO_LEVEL',
    'GEO_NAME',
    'CHARACTERISTIC_ID',
    'CHARACTERISTIC_NAME',
    'C1_COUNT_TOTAL',
    'C2_COUNT_MEN+',
    'C3_COUNT_WOMEN+',
    'C10_RATE_TOTAL',
    'C11_RATE_MEN+',
    'C12_RATE_WOMEN+'
]

dtypes = {
    'CENSUS_YEAR': np.int64,
    'DGUID': str,
    'GEO_LEVEL': str,
    'GEO_NAME': str,
    'CHARACTERISTIC_ID': np.int64,
    'CHARACTERISTIC_NAME': str,
    'C1_COUNT_TOTAL': np.double,
    'C2_COUNT_MEN+': np.double,
    'C3_COUNT_WOMEN+': np.double,
    'C10_RATE_TOTAL': np.double,
    'C11_RATE_MEN+': np.double,
    'C12_RATE_WOMEN+': np.double,    
}

with zipfile.ZipFile('./census_data/98-401-X2021006_eng_CSV.zip') as z:

    for file in z.namelist():

        if not file.endswith('.csv'):
            continue

        print(f"Processing {file}")

        output_path = f'parquet_data/{file[:-4]}.parquet'

        with z.open(file) as f:

            writer = None

            for chunk in pd.read_csv(
                f,
                encoding='latin1',
                low_memory=False,
                usecols=cols,
                dtype=dtypes,
                chunksize=100_000
            ):


                table = pa.Table.from_pandas(
                    chunk,
                    preserve_index=False,
                )


                if writer is None:
                    writer = pq.ParquetWriter(
                        output_path,
                        table.schema,
                        compression='snappy'
                    )

                writer.write_table(table)

                print(f"  processed {len(chunk):,} rows")

            if writer is not None:
                writer.close()

        print(f"Finished: {output_path}")