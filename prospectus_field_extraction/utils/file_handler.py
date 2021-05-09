import html
import json

from unidecode import unidecode

from prospectus_field_extraction import ROOT_PATH


def read_json(json_path):
    with open(ROOT_PATH / json_path, 'r') as json_file:
        return json.load(json_file)


def write_json(dic, json_path):
    with open(ROOT_PATH / json_path, 'w') as json_file:
        return json.dump(dic, json_file)


def create_file_list():
    with open(ROOT_PATH / 'data' / 'list_of_annotated_fund.json') as json_file:
        json_data = json.load(json_file)
    return [fund['prospectus'].split('/')[-1].replace('pdf', 'txt') for fund in json_data]


def read_and_clean_text(file):
    with open(ROOT_PATH / 'data' / 'raw' / file, 'r+') as f:
        text = f.read()
    return clean_text(text)


def clean_text(text):
    return html.unescape(
        unidecode(text.lower().replace('-', ' ').replace('\'', ' ').replace('ç', 'c').replace('’', ' ')))
