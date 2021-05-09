import re

from prospectus_field_extraction.model.lookup.abstract_finder import lookup_finder

GOAL_PATTERNS = ['objectif de gestion :', 'objectif de gestion']

LEMMATIZED_GOAL_TABLE = {'neer': 'Non trouvé'}


def find_goal_pattern(text):
    for field_pattern in GOAL_PATTERNS:
        for el in re.finditer(field_pattern, text):
            return text[el.end():el.end() + text[el.end():].find('.')]


def main():
    lookup_finder({}, LEMMATIZED_GOAL_TABLE, find_goal_pattern, accuracy_pattern=True)
