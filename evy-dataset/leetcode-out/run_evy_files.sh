#!/bin/zsh

# Ensure the 'passed' directory exists
mkdir -p passed

# Iterate over each .evy file in the current directory
for file in *.evy
do
    # Run the evy command on the file
    evy run "$file"

    # Capture the exit code
    exit_code=$?

    # Log the exit code and file name to results.txt
    echo "$exit_code: $file" >> results.txt

    # If the exit code is zero, move the file to the 'passed' directory
    if [ $exit_code -eq 0 ]; then
        mv "$file" passed/
    fi
done

# Sort the results.txt file in place
sort -o results.txt results.txt
