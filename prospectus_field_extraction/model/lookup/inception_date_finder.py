import re

from prospectus_field_extraction.model.lookup.abstract_finder import lookup_finder

INCEPTION_DATE_PATTERNS = ['creee le ', 'crees le ', 'cree le ', 'date de creation', 'opcvm a ete constitue le']

LEMMATIZED_INCEPTION_DATE_TABLE = {'neer': 'Non trouvé'}

LOOKUP_INCEPTION_DATE_TABLE = {k: 0 for k in LEMMATIZED_INCEPTION_DATE_TABLE.keys()}


def find_inception_date_pattern(text):
    for field_pattern in INCEPTION_DATE_PATTERNS:
        for el in re.finditer(field_pattern, text):

            text = text[el.end():el.end() + 100]
            date = re.findall(r'\d{1,2}\s\w+\s\d{2,4}', text) or re.findall(r'(\d+/\d+/\d+)', text)
            if date:
                return date[0]
            else:
                return text


def main():
    lookup_finder(LOOKUP_INCEPTION_DATE_TABLE, LEMMATIZED_INCEPTION_DATE_TABLE, find_inception_date_pattern,
                  accuracy_pattern=True)
