#!/bin/bash

mkdir raw golden app
cd raw
for f in *.pdf; do
  pdftotext -enc UTF-8 $f
done
cd ..
python build_fund_name_dataset.py
