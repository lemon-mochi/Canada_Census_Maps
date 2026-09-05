import os
import re
import zipfile
import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

# Define schemas according to native Statistics Canada layouts
CENSUS_CONFIGS = {
    2021: {
        'usecols': [
            'CENSUS_YEAR', 'DGUID', 'GEO_LEVEL', 'GEO_NAME',
            'CHARACTERISTIC_ID', 'CHARACTERISTIC_NAME',
            'C1_COUNT_TOTAL', 'C2_COUNT_MEN+', 'C3_COUNT_WOMEN+',
            'C10_RATE_TOTAL', 'C11_RATE_MEN+', 'C12_RATE_WOMEN+'
        ],
        'dtypes': {
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
        },
        'zips': [
            './census_data/98-401-X2021006_eng_CSV.zip',
            './census_data/98-401-X2021010_eng_CSV.zip',
            './census_data/98-401-X2021029_eng_CSV.zip',
            './census_data/98-401-X2021012_eng_CSV.zip'
        ]
    },
    2016: {
        'names': [
            'CENSUS_YEAR', 
            'GEO_CODE (POR)',
            'GEO_LEVEL',
            'GEO_NAME',
            'GNR',
            'GNR_LF',
            'DATA_QUALITY_FLAG',
            'ALT_GEO_CODE',
            'CHARACTERISTIC_NAME',
            'CHARACTERISTIC_ID',
            'NOTES',
            'COUNT_TOTAL',
            'COUNT_MALE',
            'COUNT_FEMALE'
        ],
        'cols': [
            'CENSUS_YEAR', 
            'GEO_CODE (POR)',
            'GEO_LEVEL',
            'GEO_NAME',
            'CHARACTERISTIC_NAME',
            'CHARACTERISTIC_ID',
            'COUNT_TOTAL',
            'COUNT_MALE',
            'COUNT_FEMALE'            

        ],
        'dtypes': {
            'CENSUS_YEAR': np.int64,
            'GEO_CODE (POR)': str,
            'GEO_LEVEL': str,
            'GEO_NAME': str,
            'GNR': np.double,
            'GNR_LF': np.double,
            'DATA_QUALITY_FLAG': str,
            'ALT_GEO_CODE': str,
            'CHARACTERISTIC_NAME': str,
            'CHARACTERISTIC_ID': np.int64,
            'COUNT_TOTAL': np.double,
            'COUNT_MALE': np.double,
            'COUNT_FEMALE': np.double
        },
        'zips': [
            './census_data/98-401-X2016044_eng_CSV.zip',
            './census_data/98-401-X2016045_eng_CSV.zip',
            './census_data/98-401-X2016050_eng_CSV.zip'
        ]
    }
}

# Regex patterns for 2016 dynamic characteristic columns
CHAR_NAME_RE = re.compile(r'^DIM:\s*Profile of.*$', re.I)
CHAR_ID_RE = re.compile(r'^Member ID:\s*Profile of.*$', re.I)

def make_column_filter(year_config):
    """Returns a callable for pd.read_csv(usecols=...)"""
    if 'usecols' in year_config:
        return lambda c: c in year_config['usecols']
    
    fixed = set(year_config['fixed_cols'])
    return lambda c: c in fixed or bool(CHAR_NAME_RE.match(c)) or bool(CHAR_ID_RE.match(c))

def process_year_data(year_config, output_path):
    writer = None
    col_filter = make_column_filter(year_config)

    for zip_path in year_config['zips']:
        if not os.path.exists(zip_path):
            print(f"Skipping missing file: {zip_path}")
            continue

        with zipfile.ZipFile(zip_path) as z:
            for file in z.namelist():
                if not file.endswith('.csv'):
                    continue

                print(f"Processing {file}")

                with z.open(file) as f:
                    for chunk in pd.read_csv(
                        f,
                        encoding='latin1',
                        low_memory=False,
                        usecols=col_filter,
                        dtype=year_config['dtypes'],
                        chunksize=100_000
                    ):

                        table = pa.Table.from_pandas(chunk, preserve_index=False)

                        if writer is None:
                            writer = pq.ParquetWriter(
                                output_path,
                                table.schema,
                                compression='snappy'
                            )

                        writer.write_table(table)
                        print(f"  processed {len(chunk):,} rows")

    if writer:
        writer.close()
        print(f"Finished writing: {output_path}")

def process_2016_data(year_config, output_path):
    writer = None

    for zip_path in year_config['zips']:
        if not os.path.exists(zip_path):
            print(f"Skipping missing file: {zip_path}")
            continue        

        with zipfile.ZipFile(zip_path) as z:
            for file in z.namelist():
                if not file.endswith('.csv'):
                    continue

                if file == 'Geo_starting_row_CSV.csv':
                    print('here')
                    continue                

                print(f"Processing {file}")
                with z.open(file) as f:
                    for chunk in pd.read_csv(
                        f,
                        encoding='utf-8-sig',
                        low_memory=False,
                        header=0,
                        names=year_config['names'],
                        dtype=year_config['dtypes'],
                        na_values=['x', 'X', '..', 'F', '...', 'null', 'NULL'],
                        chunksize=100_000
                    ):
                        chunk = chunk[year_config['cols']]

                        table = pa.Table.from_pandas(chunk, preserve_index=False)

                        if writer is None:
                            writer = pq.ParquetWriter(
                                output_path,
                                table.schema,
                                compression='snappy'
                            )

                        writer.write_table(table)
                        print(f"  processed {len(chunk):,} rows")

    if writer:
        writer.close()
        print(f"Finished writing: {output_path}")
            

# Run pipeline per year
for year, config in CENSUS_CONFIGS.items():
    output_dir = f"temp_parquet_data/census_{year}"
    os.makedirs(output_dir, exist_ok=True)

    out_file = os.path.join(
        output_dir,
        f"{year}_raw_census_data.parquet"
    )

    if year == 2016:
        process_2016_data(config, out_file)
    else:
        process_year_data(config, out_file)