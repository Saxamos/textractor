#!/bin/bash

# shellcheck disable=SC2164
cd prospectus_field_extraction/data
mkdir raw
cd raw
# shellcheck disable=SC2002
cat ../list_of_annotated_fund.json | raw ".map('prospectus').join('\n')" | parallel curl -O
