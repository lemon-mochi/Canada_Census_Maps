#!/usr/bin/env bash

set -e

OUTPUT_DIR="${1:-../tiles_output}"

mkdir -p "$OUTPUT_DIR"

ensure_utf8() {
    local input_file="$1"
    local output_file="$2"

    # If already valid UTF-8, copy unchanged.
    if iconv -f UTF-8 -t UTF-8 "$input_file" > "$output_file" 2>/dev/null; then
        return
    fi

    # Otherwise assume ISO-8859-1.
    iconv -f ISO-8859-1 -t UTF-8 "$input_file" > "$output_file"
}

process_directory() {
    local input_dir="$1"

    shopt -s nullglob globstar
    local geojson_files=("$input_dir"/**/*.geojson)

    if [ ${#geojson_files[@]} -eq 0 ]; then
        echo "No .geojson files found in $input_dir"
        return
    fi

    echo "Found ${#geojson_files[@]} GeoJSON files in $input_dir"
    echo "----------------------------------------------------"

    for file in "${geojson_files[@]}"; do
        filename=$(basename "$file" .geojson)
        output_file="$OUTPUT_DIR/${filename}.pmtiles"

        echo "Processing: $file"
        echo "Output:     $output_file"

        temp_file=$(mktemp --suffix=.geojson)
        trap 'rm -f "$temp_file"' EXIT

        ensure_utf8 "$file" "$temp_file"

        tippecanoe \
            -o "$output_file" \
            -zg \
            -Z4 \
            --drop-densest-as-needed \
            --extend-zooms-if-still-dropping \
            --force \
            -L "$filename:$temp_file"

        rm -f "$temp_file"
        trap - EXIT

        echo "Finished $filename.pmtiles"
        echo "----------------------------------------------------"
    done
}

# 2006-2021
process_directory "./geojson"

# 1981-2001
process_directory "./1981-2001_geojson"

echo "All GeoJSON files successfully converted to PMTiles in $OUTPUT_DIR!"