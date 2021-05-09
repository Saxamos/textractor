import re

from prospectus_field_extraction.model.lookup.abstract_finder import lookup_finder

CLOSING_DATE_PATTERNS = ['date de cloture de l exercice comptable', 'date de cloture de l exercice',
                         'date de cloture']

LEMMATIZED_CLOSING_DATE_TABLE = {'neer': 'Non trouvé'}

LOOKUP_CLOSING_DATE_TABLE = {k: 0 for k in LEMMATIZED_CLOSING_DATE_TABLE.keys()}


def find_closing_date_pattern(text):
    for field_pattern in CLOSING_DATE_PATTERNS:
        for el in re.finditer(field_pattern, text):
            text = text[el.end():el.end() + 100]
            if text.find('.') != -1:
                return text[: text.find('.')]
            elif text.find('(') != -1:
                return text[:text.find('(')]
            else:
                return text


def main():
    lookup_finder(LOOKUP_CLOSING_DATE_TABLE, LEMMATIZED_CLOSING_DATE_TABLE, find_closing_date_pattern,
                  accuracy_pattern=True)
