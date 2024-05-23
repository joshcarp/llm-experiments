#!/bin/zsh

# Ensure the 'passed' directory exists
mkdir -p passed
echo "" > results.txt

# Iterate over each .evy file in the current directory
passed=0
failed=0
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
        ((passed++))  # Correct way to increment in Zsh
        mv "$file" passed/  # Uncomment if you want to move passed files
    fi
    if [ $exit_code -eq 1 ]; then
        ((failed++))  # Correct way to increment in Zsh
    fi
done

echo "passed: $passed" >> results.txt
echo "failed: $failed" >> results.txt

# Sort the results.txt file in place
sort -o results.txt results.txt
