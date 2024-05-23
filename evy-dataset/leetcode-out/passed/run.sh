#!/bin/zsh

for file in *.evy
do
    echo "running $file"
    evy run "$file"
done
