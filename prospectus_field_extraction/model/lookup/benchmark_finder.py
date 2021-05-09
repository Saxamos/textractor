import re

from prospectus_field_extraction.model.lookup.abstract_finder import lookup_finder

BENCHMARK_PATTERNS = ['indicateur de reference :', ]

LEMMATIZED_BENCHMARK_TABLE = {'neer': 'Pas d\'indicateur de référence'}


def find_benchmark_pattern(text):
    for field_pattern in BENCHMARK_PATTERNS:
        for el in re.finditer(field_pattern, text):
            return text[el.end():el.end() + text[el.end():].find('.')]


def main():
    lookup_finder({}, LEMMATIZED_BENCHMARK_TABLE, find_benchmark_pattern, accuracy_pattern=True)
