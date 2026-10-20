"""
This file was my attempt at using an API to get 2011 NHS data. It did not work well due to rate limits.
Read 2011_NHS_Data.md in the root directory for more information.
THERE IS NO NEED TO RUN THIS FILE.
"""

import pycancensus as pc
import pandas as pd
from dotenv import load_dotenv
import os
from pathlib import Path
from datetime import datetime, timedelta
import json
import time


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

load_dotenv()

api_key = os.getenv("API_KEY")
pc.set_api_key(api_key)

DATASET = "CA11"

PROVINCES = [
    "10",
    "11",
    "12",
    "13",
    "24",
    "35",
    "46",
    "47",
    "48",
    "59",
    "60",
    "61",
    "62",
]

# Keep this small because the API is very restrictive.
CHUNK_SIZE = 10

# Stay below the actual limits to leave some safety margin.
HOURLY_LIMIT = 900
DAILY_LIMIT = 9000

OUTPUT_DIR = Path("2011_NHS_DA")
OUTPUT_DIR.mkdir(exist_ok=True)

REQUEST_LOG = OUTPUT_DIR / "request_log.json"


# ---------------------------------------------------------
# Request tracking
# ---------------------------------------------------------

if REQUEST_LOG.exists():
    with open(REQUEST_LOG, "r") as f:
        request_times = json.load(f)
else:
    request_times = []


def save_request_log():
    with open(REQUEST_LOG, "w") as f:
        json.dump(request_times, f)


def clean_request_log():
    """
    Remove requests older than 24 hours.
    """
    global request_times

    now = datetime.now()
    cutoff = now - timedelta(hours=24)

    request_times = [
        timestamp
        for timestamp in request_times
        if datetime.fromisoformat(timestamp) > cutoff
    ]


def wait_for_rate_limit():
    """
    Wait if we are approaching either API limit.
    """

    global request_times

    clean_request_log()

    now = datetime.now()

    # Requests made in the last hour
    one_hour_ago = now - timedelta(hours=1)

    hourly_requests = [
        timestamp
        for timestamp in request_times
        if datetime.fromisoformat(timestamp) > one_hour_ago
    ]

    # Requests made in the last 24 hours
    daily_requests = len(request_times)

    print()
    print(
        f"Requests: {len(hourly_requests)} this hour, "
        f"{daily_requests} in last 24 hours"
    )

    # -----------------------------------------------------
    # Hourly limit
    # -----------------------------------------------------

    if len(hourly_requests) >= HOURLY_LIMIT:

        oldest = min(datetime.fromisoformat(timestamp) for timestamp in hourly_requests)

        wait_until = oldest + timedelta(hours=1)

        wait_seconds = (wait_until - now).total_seconds()

        if wait_seconds > 0:

            print()
            print("=" * 60)
            print("HOURLY LIMIT REACHED")
            print("=" * 60)

            print(f"Waiting {wait_seconds / 60:.1f} minutes " f"before continuing...")

            time.sleep(wait_seconds)

            # Recheck after sleeping
            return wait_for_rate_limit()

    # -----------------------------------------------------
    # Daily limit
    # -----------------------------------------------------

    if daily_requests >= DAILY_LIMIT:

        oldest = min(datetime.fromisoformat(timestamp) for timestamp in request_times)

        wait_until = oldest + timedelta(hours=24)

        wait_seconds = (wait_until - now).total_seconds()

        print()
        print("=" * 60)
        print("DAILY LIMIT REACHED")
        print("=" * 60)

        print(f"9,000 requests have been made in the " f"last 24 hours.")

        print(f"Waiting {wait_seconds / 3600:.1f} hours " f"before continuing...")

        time.sleep(wait_seconds)

        return wait_for_rate_limit()


def record_request():
    """
    Record an API request before making it.
    """
    global request_times

    request_times.append(datetime.now().isoformat())

    save_request_log()


# ---------------------------------------------------------
# Get vectors
# ---------------------------------------------------------

print("Getting list of Census vectors...")

vectors = pc.list_census_vectors(DATASET)

vectors = vectors[vectors["details"].str.contains("CA 2011 NHS", case=False, na=False)]

vectors = vectors["vector"].tolist()

print(f"Found {len(vectors)} NHS vectors.")


# ---------------------------------------------------------
# Split vectors into chunks
# ---------------------------------------------------------

chunks = [vectors[i : i + CHUNK_SIZE] for i in range(0, len(vectors), CHUNK_SIZE)]

print(f"Using {len(chunks)} chunks " f"of {CHUNK_SIZE} vectors.")

print(f"Maximum possible API requests: " f"{len(PROVINCES) * len(chunks):,}")


# ---------------------------------------------------------
# Download
# ---------------------------------------------------------

for province in PROVINCES:

    province_dir = OUTPUT_DIR / province
    province_dir.mkdir(exist_ok=True)

    print()
    print("=" * 60)
    print(f"PROVINCE: {province}")
    print("=" * 60)

    for chunk_number, chunk in enumerate(chunks):

        output_file = province_dir / f"chunk_{chunk_number:04d}.csv"

        # -------------------------------------------------
        # Resume support
        # -------------------------------------------------

        if output_file.exists():

            print(f"Skipping chunk " f"{chunk_number + 1}/{len(chunks)}")

            continue

        # -------------------------------------------------
        # Rate-limit check
        # -------------------------------------------------

        wait_for_rate_limit()

        print()
        print(
            f"Downloading chunk "
            f"{chunk_number + 1}/{len(chunks)} "
            f"({len(chunk)} vectors)"
        )

        print(f"Province: {province}")

        # Count this request
        record_request()

        try:

            df = pc.get_census(
                dataset=DATASET,
                regions={"PR": province},
                vectors=chunk,
                level="DA",
                geo_format=None,
                labels="short",
            )

            print(f"Downloaded {len(df):,} rows.")

            # Save immediately
            df.to_csv(output_file, index=False)

            print(f"Saved: {output_file}")

        except Exception as e:

            print()
            print("=" * 60)
            print("ERROR")
            print("=" * 60)

            print(e)

            print()
            print(f"Failed at province {province}, " f"chunk {chunk_number}.")

            print(
                "The request has already been counted "
                "because it was sent to the API."
            )

            print("Run the script again to resume.")

            raise


print()
print("=" * 60)
print("ALL DOWNLOADS COMPLETE")
print("=" * 60)
