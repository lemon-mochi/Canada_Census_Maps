import os
import pandas as pd
import subprocess
import tempfile
from pyspark.sql.functions import col, expr, lit, when, create_map
from itertools import chain
from pyspark.sql import SparkSession


# Define schemas according to native Statistics Canada layouts
CENSUS_CONFIGS = {
    2006: {
        'zips': [
            './census_data/94-581-XCB2006002.ZIP',
            './census_data/94-581-XCB2006005.ZIP',
            './census_data/94-581-XCB2006007.ZIP',
        ],
        'xml_mappings': 'xml_mappings/2006_xml_id_mappings.csv'
    },
    2001: {
        'zips': [
            './census_data/95F0495XCB2001002.ZIP',
            './census_data/95F0495XCB2001005.ZIP',
            './census_data/95F0495XCB2001007.ZIP'
        ],
        'xml_mappings': 'xml_mappings/2001_xml_id_mappings.csv'
    }
}

output_dir = "temp_parquet_data"
os.makedirs(output_dir, exist_ok=True)


def extract_value(df, concept):
    """
    Extract a value from generic:SeriesKey.generic:Value
    based on the concept attribute.

    Returns NULL if the concept does not exist.
    """
    return expr(f"""
        filter(
            `generic:SeriesKey`.`generic:Value`,
            x -> x._concept = '{concept}'
        )[0]._value
    """)

def get_xml_mappings(xml_mappings):
    mapping_df = pd.read_csv(
        xml_mappings
    )

    characteristic_mappings = {}

    for source_column in mapping_df.columns[1:]:
        mapping = {}

        for _, row in mapping_df.iterrows():
            canonical_id = row["Characteristic_ID"]
            source_id = row[source_column]

            if pd.notna(source_id):
                mapping[str(int(source_id))] = int(canonical_id)

        characteristic_mappings[source_column] = mapping

    return characteristic_mappings

def debug_xml_data(spark, year_config):
    characteristic_mappings = get_xml_mappings(year_config["xml_mappings"])

    print("Available mappings:")
    for name, mapping in characteristic_mappings.items():
        print(f"  {name}: {len(mapping)} IDs")

    with tempfile.TemporaryDirectory() as temp_dir:

        for zip_path in year_config["zips"]:
            print(f"\n{'=' * 80}")
            print(f"ZIP: {zip_path}")
            print(f"{'=' * 80}")

            result = subprocess.run(
                ["unzip", "-Z1", zip_path],
                capture_output=True,
                text=True,
                check=True,
            )

            xml_files = [
                name
                for name in result.stdout.splitlines()
                if name.lower().endswith(".xml")
                and not os.path.basename(name).startswith("Structure")
            ]

            print(f"Found {len(xml_files)} XML files")

            for i, xml_name in enumerate(xml_files, start=1):
                print(f"\n{'-' * 80}")
                print(f"[{i}/{len(xml_files)}] {xml_name}")
                print(f"{'-' * 80}")

                xml_path = os.path.join(temp_dir, "input.xml")

                with open(xml_path, "wb") as f:
                    subprocess.run(
                        ["unzip", "-p", zip_path, xml_name],
                        stdout=f,
                        check=True,
                    )

                df = (
                    spark.read.format("xml")
                    .option("rowTag", "generic:Series")
                    .load(f"file://{xml_path}")
                )

                source_name = os.path.basename(xml_name)[8:-4]

                print(f"Source name: {source_name}")

                if source_name not in characteristic_mappings:
                    print("ERROR: No mapping found!")
                    print(
                        "Available mapping names:",
                        list(characteristic_mappings.keys()),
                    )
                    os.remove(xml_path)
                    continue

                mapping = characteristic_mappings[source_name]

                print(f"Mapping contains {len(mapping)} IDs")
                print("First 20 mappings:")
                print(dict(list(mapping.items())[:20]))

                # First inspect the raw values.
                raw_result = df.select(
                    extract_value(df, "GEO").alias("GEO_CODE"),
                    extract_value(df, "DIM0").alias("SOURCE_DIM0"),
                    col("generic:Obs.generic:Time").alias("CENSUS_YEAR"),
                    col("generic:Obs.generic:ObsValue._value").alias("COUNT_TOTAL"),
                )

                print("\nRaw data:")
                raw_result.show(20, truncate=False)

                # Show the actual SeriesKey so we can see all dimensions.
                print("\nRaw SeriesKey:")
                df.select(
                    "generic:SeriesKey"
                ).show(10, truncate=False)

                # Apply the mapping, but do NOT write anything.
                mapping_expr = create_map(
                    *chain.from_iterable(
                        (lit(source_id), lit(canonical_id))
                        for source_id, canonical_id in mapping.items()
                    )
                )

                debug_result = raw_result.withColumn(
                    "CHARACTERISTIC_ID",
                    mapping_expr[col("SOURCE_DIM0").cast("string")],
                )

                debug_result = debug_result.select(
                    "GEO_CODE",
                    "SOURCE_DIM0",
                    "CHARACTERISTIC_ID",
                    "CENSUS_YEAR",
                    "COUNT_TOTAL",
                )

                print("\nMapped data:")
                debug_result.show(30, truncate=False)

                # Find DIM0 values that did not map.
                print("\nUnmapped DIM0 values:")

                unmapped = (
                    debug_result
                    .filter(col("CHARACTERISTIC_ID").isNull())
                    .select("SOURCE_DIM0")
                    .distinct()
                )

                unmapped.show(100, truncate=False)

                # Show counts by characteristic.
                print("\nCounts by mapped CHARACTERISTIC_ID:")

                (
                    debug_result
                    .groupBy("CHARACTERISTIC_ID")
                    .count()
                    .orderBy("CHARACTERISTIC_ID")
                    .show(100, truncate=False)
                )

                os.remove(xml_path)

out_file = os.path.join(
    output_dir,
    "2006_raw_census_data.parquet"
)

spark = (
    SparkSession.builder
    .appName("2006 Census")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("ERROR")

# this will take a very long time

debug_xml_data(
    spark,
    CENSUS_CONFIGS[2006],
)

spark.stop()