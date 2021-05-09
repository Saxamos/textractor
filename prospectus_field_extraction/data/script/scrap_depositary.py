from urllib.request import urlopen

from bs4 import BeautifulSoup
from tqdm import tqdm
from unidecode import unidecode

from prospectus_field_extraction.utils.file_handler import write_json


def main():
    lemmatized_depositary_table = _scrap_depositary()
    write_json(lemmatized_depositary_table, 'data/lemmatized_depositary_table.json')


def _scrap_depositary():
    lemmatized_depositary_table = dict()
    for i in tqdm(range(1, 8)):
        url = f'https://funds360.euronext.com/acteur/societes/liste/depositaire/page/{i}'
        html = urlopen(url).read()
        soup = BeautifulSoup(html, features='html.parser')
        for name in soup.findAll('div', {'class': 'box-cont'})[0].findAll('a', {'class': 'name'}):
            lemmatized_depositary_table[unidecode(name.text.lower())] = name.text
    return lemmatized_depositary_table


if __name__ == '__main__':
    main()
