#!/bin/bash

for file in *.evy; do
    evy run $file
done
