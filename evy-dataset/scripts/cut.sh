#!/bin/bash

for file in *.evy; do
    if [ -f "$file" ]; then
        filename="${file%.evy}"
        first_line=$(head -n 1 "$file")  # Extract the first line
        modified_line="${first_line:2}"  # Cut the first two characters
        echo "$modified_line" > "${filename}-input.txt"
    fi
done
