import pycancensus as pc
from dotenv import load_dotenv
import os

load_dotenv()

pc.set_api_key(os.getenv("API_KEY"))

vectors = pc.list_census_vectors("CA11")

vectors = vectors[
    vectors["details"].str.contains(
        "CA 2011 NHS",
        case=False,
        na=False
    )
]

print(f"NHS vectors: {len(vectors)}")

# Just ONE vector
test_vector = vectors["vector"].iloc[0]

print("Testing vector:", test_vector)

df = pc.get_census(
    dataset="CA11",
    regions={"PR": "10"},
    vectors=[test_vector],
    level="DA",
    geo_format=None,
    labels="short"
)

print(df.head())
print(f"Rows: {len(df)}")