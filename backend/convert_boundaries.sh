#!/usr/bin/env bash

# Exit immediately if a command exits with a non-zero status
set -e

# # Directory containing 2006-2021 GeoJSON files and merged geojson from merge_split_geojson.py
# INPUT_DIR="${1:-./geojson}"
# OUTPUT_DIR="${2:-./tiles_output}"

# # Create the output directory if it doesn't exist
# mkdir -p "$OUTPUT_DIR"

# # Enable nullglob so the loop doesn't fail if no .geojson files exist
# shopt -s nullglob
# geojson_files=("$INPUT_DIR"/*.geojson)

# if [ ${#geojson_files[@]} -eq 0 ]; then
#     echo "No .geojson files found in $INPUT_DIR"
#     exit 1
# fi

# echo "Found ${#geojson_files[@]} GeoJSON files to process..."
# echo "----------------------------------------------------"

# for file in "${geojson_files[@]}"; do
#     # Extract filename without directory or extension
#     filename=$(basename "$file" .geojson)
#     output_file="$OUTPUT_DIR/${filename}.pmtiles"

#     echo "Processing: $file"
#     echo "Output:     $output_file"

#     # Execute tippecanoe
#     # -o: output PMTiles file
#     # -zg: automatically calculate maximum zoom level based on feature density
#     # -Z4: minimum zoom level (adjust based on your app's needs)
#     # --drop-densest-as-needed: drops dense features automatically at zoomed-out levels to keep tiles small
#     # --extend-zooms-if-still-dropping: ensures details aren't lost if maxzoom was guessed too low
#     # --force: overwrites the output file if it already exists
#     tippecanoe \
#         -o "$output_file" \
#         -zg \
#         -Z4 \
#         --drop-densest-as-needed \
#         --extend-zooms-if-still-dropping \
#         --force \
#         "$file"

#     echo "Finished $filename.pmtiles"
#     echo "----------------------------------------------------"
# done

INPUT_DIR="${1:-./1981-2001_geojson}"
OUTPUT_DIR="${2:-./tiles_output}"

shopt -s nullglob globstar
geojson_files=("$INPUT_DIR"/**/*.geojson)

if [ ${#geojson_files[@]} -eq 0 ]; then
    echo "No .geojson files found in $INPUT_DIR"
    exit 1
fi

echo "Found ${#geojson_files[@]} GeoJSON files to process..."
echo "----------------------------------------------------"

for file in "${geojson_files[@]}"; do
    # Extract filename without directory or extension
    filename=$(basename "$file" .geojson)
    output_file="$OUTPUT_DIR/${filename}.pmtiles"

    echo "Processing: $file"
    echo "Output:     $output_file"

    # Execute tippecanoe
    # -o: output PMTiles file
    # -zg: automatically calculate maximum zoom level based on feature density
    # -Z4: minimum zoom level (adjust based on your app's needs)
    # --drop-densest-as-needed: drops dense features automatically at zoomed-out levels to keep tiles small
    # --extend-zooms-if-still-dropping: ensures details aren't lost if maxzoom was guessed too low
    # --force: overwrites the output file if it already exists
    tippecanoe \
        -o "$output_file" \
        -zg \
        -Z4 \
        --drop-densest-as-needed \
        --extend-zooms-if-still-dropping \
        --force \
        "$file"

    echo "Finished $filename.pmtiles"
    echo "----------------------------------------------------"
done


echo "All GeoJSON files successfully converted to PMTiles in $OUTPUT_DIR!"