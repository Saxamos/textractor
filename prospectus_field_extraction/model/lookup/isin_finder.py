import re

from prospectus_field_extraction.model.lookup.abstract_finder import lookup_finder

LEMMATIZED_ISIN_TABLE = {'neer': 'Non trouvé'}


def find_isin_pattern(text):
    isin_list = {match.group().upper() for match in re.finditer(r'\b([a-z]{2})((?![a-z]{10}\b)[a-z0-9]{10})\b', text)}
    return isin_list


def main():
    lookup_finder({}, LEMMATIZED_ISIN_TABLE, find_isin_pattern, accuracy_pattern=True)
