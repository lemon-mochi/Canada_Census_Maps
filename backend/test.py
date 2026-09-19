import os
import tempfile
import zipfile
from pyspark.sql import SparkSession

# Initialize Spark without external package configuration
spark = (
    SparkSession.builder
    .appName("2006 Census")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("ERROR")

def process_2006_zip(zip_path):
    with tempfile.TemporaryDirectory() as temp_dir:
        with zipfile.ZipFile(zip_path) as z:
            xml_files = [
                name
                for name in z.namelist()
                if name.endswith(".xml") and not name.startswith("Structure")
            ]

            for name in xml_files:
                z.extract(name, temp_dir)

        # Spark natively handles XML format in newer versions
        df = (
            spark.read.format("xml")
            .option("rowTag", "generic:Series")
            .load(f"file://{os.path.abspath(temp_dir)}")
        )

        df.printSchema()
        df.show(5)

process_2006_zip('./census_data/94-581-XCB2006007.ZIP')