#!/bin/bash

# Check if an argument is provided
if [ $# -eq 0 ]; then
    echo "Usage: $0 <odt_file>"
    exit 1
fi

# Get the input ODT file path
odt_file="$1"


# Check if the file exists
if [ ! -f "$odt_file" ]; then
    echo "File not found: $odt_file"
    exit 1
fi

# Convert ODT file to HTML using ofpy2xhtml
converted_html=$(odf2xhtml "$odt_file")

# Extract filename without extension
filename=$(basename -- "$odt_file")
filename_no_ext="${filename%.*}"

# Call your Python script with converted HTML and filename
python3 HTML_parser.py "$converted_html" "$filename_no_ext"

# Optionally, display a success message
echo "Conversion and processing completed successfully."