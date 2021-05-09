import re

from prospectus_field_extraction.model.lookup.abstract_finder import lookup_finder
from prospectus_field_extraction.utils.file_handler import read_json

DEPOSITARY_PATTERNS = ['depositaire :', 'le depositaire de']

LEMMATIZED_DEPOSITARY_TABLE = read_json('model/lookup/depositary_table.json')

LOOKUP_DEPOSITARY_TABLE = {k: 0 for k in LEMMATIZED_DEPOSITARY_TABLE.keys()}


def find_depositary_pattern(text):
    for field_pattern in DEPOSITARY_PATTERNS:
        for el in re.finditer(field_pattern, text):
            return text[el.start():el.end() + 100]


def main():
    lookup_finder(LOOKUP_DEPOSITARY_TABLE, LEMMATIZED_DEPOSITARY_TABLE, find_depositary_pattern)
