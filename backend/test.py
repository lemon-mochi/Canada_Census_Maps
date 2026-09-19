import os
import tempfile
import zipfile
import shutil
from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("2006 Census")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("ERROR")


def process_2006_zip(zip_path, output_path):
    with tempfile.TemporaryDirectory() as temp_dir:
        with zipfile.ZipFile(zip_path) as z:
            xml_files = [
                name
                for name in z.namelist()
                if name.endswith(".xml") and not name.startswith("Structure")
            ]

            for name in xml_files:
                z.extract(name, temp_dir)

        df = (
            spark.read.format("xml")
            .option("rowTag", "generic:Series")
            .load(f"file://{os.path.abspath(temp_dir)}")
        )

        # Spark writes to a directory, so use a temporary directory first.
        temp_output = output_path + "_tmp"

        df.coalesce(1).write \
            .format("parquet") \
            .mode("overwrite") \
            .option("compression", "snappy") \
            .save(temp_output)

        # Find the single generated parquet file.
        part_file = next(
            os.path.join(temp_output, f)
            for f in os.listdir(temp_output)
            if f.startswith("part-") and f.endswith(".parquet")
        )

        # Move it to the desired filename.
        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
        shutil.move(part_file, output_path)

        # Remove Spark's temporary output directory.
        shutil.rmtree(temp_output)


process_2006_zip(
    "./census_data/94-581-XCB2006007.ZIP",
    "./test/2006_census.parquet"
)