import boto3
import os

s3 = boto3.client("s3", region_name="us-east-1")


def get_tile_url(census_year: int, geo_level: str) -> str:
    """Generate a temporary pre-signed URL for a PMTiles file."""
    filename = _get_tile_filename(census_year, geo_level)
    key = f"{S3_PREFIX_TILES}/{filename}" if S3_PREFIX_TILES else filename

    url = s3.generate_presigned_url(
        "get_object",
        Params={"Bucket": BUCKET_NAME, "Key": key},
        ExpiresIn=3600,  # URL valid for 1 hour
    )
    return url
