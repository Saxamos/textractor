#!/bin/bash

# shellcheck disable=SC2164
cd prospectus_field_extraction/data/raw
for f in *.pdf; do
  echo "$f"
  pdftotext -enc UTF-8 "$f"
done
cd ../../..
