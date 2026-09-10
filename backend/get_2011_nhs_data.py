import pycancensus as pc
import pandas as pd
from dotenv import load_dotenv
import os
from pathlib import Path
import time

load_dotenv()

api_key = os.getenv("API_KEY")
pc.set_api_key(api_key)

DATASET = "CA11"

PROVINCES = [
    "10", "11", "12", "13", "24", "35",
    "46", "47", "48", "59", "60", "61", "62"
]

CHUNK_SIZE = 100

OUTPUT_DIR = Path("2011_NHS_DA")
OUTPUT_DIR.mkdir(exist_ok=True)


# Get vectors
print("Getting list of Census vectors...")

vectors = pc.list_census_vectors(DATASET)

# Keep only 2011 NHS vectors
vectors = vectors[
    vectors["details"].str.contains(
        "CA 2011 NHS",
        case=False,
        na=False
    )
]

vectors = vectors["vector"].tolist()

print(f"Found {len(vectors)} NHS vectors.")

# Split vectors into chunks
chunks = [
    vectors[i:i + CHUNK_SIZE]
    for i in range(0, len(vectors), CHUNK_SIZE)
]

print(f"Using {len(chunks)} chunks of up to {CHUNK_SIZE} vectors each.")


# Download province by province
for province in PROVINCES:

    province_dir = OUTPUT_DIR / province
    province_dir.mkdir(exist_ok=True)

    print()
    print("=" * 60)
    print(f"PROVINCE: {province}")
    print("=" * 60)

    for chunk_number, chunk in enumerate(chunks):

        output_file = province_dir / f"chunk_{chunk_number:03d}.csv"

        # Skip chunks that were already downloaded
        if output_file.exists():
            print(
                f"Skipping chunk {chunk_number + 1}/{len(chunks)} "
                f"(already downloaded)"
            )
            continue

        print()
        print(
            f"Downloading chunk {chunk_number + 1}/{len(chunks)} "
            f"({len(chunk)} vectors)..."
        )

        try:
            df = pc.get_census(
                dataset=DATASET,
                regions={"PR": province},
                vectors=chunk,
                level="DA",
                geo_format=None,
                labels="short"
            )

            print(f"Downloaded {len(df):,} rows.")

            # Save immediately
            df.to_csv(output_file, index=False)

            print(f"Saved: {output_file}")

        except Exception as e:
            print()
            print(f"ERROR:")
            print(e)
            print()
            print(
                f"Stopping at province {province}, "
                f"chunk {chunk_number}."
            )
            print("Run the script again to resume.")
            raise

print()
print("All chunks downloaded.")