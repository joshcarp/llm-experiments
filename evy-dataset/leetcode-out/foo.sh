#!/bin/bash

set -eo pipefail

FILES=(*.evy)

for file in "${FILES[@]}"; do
  printf "%7s " "${file}"
  evy run "$file" || true
done// output:
//line 1 column 1: illegal character "#"
//line 7 column 26: illegal character ";"
//line 9 column 19: illegal character "|"
//line 9 column 20: illegal character "|"
