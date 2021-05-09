import re

from tqdm import tqdm

from prospectus_field_extraction import ROOT_PATH
from prospectus_field_extraction.utils.file_handler import read_json, read_and_clean_text, write_json, clean_text

FUND_NAME_LABEL = 'FUND_NAME'


def main():
    mapping_file_fund_name = _create_mapping_file_fund_name()
    fund_name_annotated_data, file_error = _build_fund_name_annotated_data(mapping_file_fund_name)
    _save_data(fund_name_annotated_data)
    print(f'\nNumber of error: {file_error}.')
    print(f'Dataset build: {len(mapping_file_fund_name)} prospectus annotated in {len(fund_name_annotated_data)} rows.')


def _create_mapping_file_fund_name():
    json_data = read_json('data/list_of_annotated_fund.json')
    return {fund['prospectus'].split('/')[-1].replace('pdf', 'txt'): clean_text(fund['fund']) for fund in json_data}


def _build_fund_name_annotated_data(mapping_file_fund_name):
    file_error = 0
    fund_name_annotated_data = []
    for file, fund_name in tqdm(mapping_file_fund_name.items()):
        try:
            text = read_and_clean_text(file)
            chunks = text.split('\n\n')
            for chunk in chunks:
                if len(chunk) < 3:
                    continue
                ner_annotation = (file, chunk, {'entities': [(el.start(), el.end(), FUND_NAME_LABEL)
                                                             for el in re.finditer(re.escape(fund_name), chunk)]})
                fund_name_annotated_data.append(ner_annotation)
        except (UnicodeDecodeError, FileNotFoundError) as e:
            # print(f'Error in file {file}: {e}')
            file_error += 1
    return fund_name_annotated_data, file_error


def _save_data(fund_name_annotated_data):
    output_dir = ROOT_PATH / 'data' / 'golden'
    if not output_dir.exists():
        output_dir.mkdir()
    write_json(fund_name_annotated_data, 'data/golden/annotated_data.json')
