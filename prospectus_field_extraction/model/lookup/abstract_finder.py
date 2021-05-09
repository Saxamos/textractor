"""
This script finds specific fields in prospectus.
You should manually add unique fields in `unique_<field_name>.json`.
Uncomment print lines to see the logs and debug problems when new prospectus are used.
"""
from pprint import pprint

import spacy
from tqdm import tqdm

from prospectus_field_extraction.utils.file_handler import create_file_list, read_and_clean_text

NOTHING_FOUND_IN_PATTERN = 'NOTHING FOUND IN PATTERN'
PATTERN_NOT_FOUND_IN_PDF = 'PATTERN NOT FOUND IN PDF'


def lookup_finder(lookup_table, lemmatized_table, find_pattern_func, start_file=0, end_file=-1, accuracy_pattern=False):
    nlp = spacy.load('fr_core_news_md')
    files = create_file_list()[start_file:end_file]
    file_pattern_mapping, file_error = _compute_file_pattern_mapping(files, find_pattern_func)
    file_field_mapping, lookup_table = _filter_pattern(file_pattern_mapping, lookup_table, lemmatized_table, nlp)
    number_of_file = len(files)
    number_of_read_file = number_of_file - file_error
    number_of_field_found = sum(lookup_table.values())
    if not accuracy_pattern:
        accuracy = number_of_field_found * 100 / number_of_read_file
        pprint(lookup_table)
    else:
        accuracy = len([el for el in file_field_mapping.values() if 'NOTHING FOUND IN PATTERN' in el]) *100/ len(
            file_field_mapping)

    pprint(file_field_mapping)
    print('\nNumber of file:', number_of_file)
    print('Number of file read:', number_of_read_file)
    print('Number of field found:', number_of_field_found)
    print(f'Accuracy: {accuracy :.2f}%\n')


def _compute_file_pattern_mapping(files, find_pattern_func):
    file_error = 0
    file_pattern_mapping = {}
    for file in tqdm(files):
        try:
            text = read_and_clean_text(file)

            pattern = find_pattern_func(text)
            if not pattern:
                pattern = PATTERN_NOT_FOUND_IN_PDF
            file_pattern_mapping[file] = pattern

        except (UnicodeDecodeError, FileNotFoundError):
            # print(f'Error in file: {file}.')
            file_error += 1
    return file_pattern_mapping, file_error


def _filter_pattern(file_pattern_mapping, lookup_table, lemmatized_table, nlp):
    file_field_mapping = {}
    for file, pattern in file_pattern_mapping.items():

        """Pattern matching (e.g. ISIN)"""
        if type(pattern) == set:
            file_field_mapping[file] = ', '.join(pattern)
            continue

        """Not found"""
        file_field_mapping[file] = PATTERN_NOT_FOUND_IN_PDF
        if pattern == PATTERN_NOT_FOUND_IN_PDF:
            # print(file, PATTERN_NOT_FOUND_IN_PDF)
            continue

        """Official name (e.g. classification)"""
        found = False
        lemmatized_pattern = ' '.join([token.lemma_ for token in nlp(pattern)])
        for field in lookup_table.keys():
            if field in lemmatized_pattern:
                found = True
                lookup_table[field] += 1
                file_field_mapping[file] = lemmatized_table[field]
                break

        """Whole sentence or specific rules (e.g. goal or date)"""
        if not found:
            file_field_mapping[file] = f'{NOTHING_FOUND_IN_PATTERN} "{lemmatized_pattern}"'
            # print(file, lemmatized_pattern)

    return file_field_mapping, lookup_table
