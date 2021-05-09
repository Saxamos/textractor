"""json file will look like this:
[{
    "shares": [
      {
        "isin": "FR0010674507",
        "url": "https://geco.amf-france.org/Bio/info_part.aspx?prev=part&NumProd=1872&NumPart=39431"
      },
      {
        "isin": "FR0013319829",
        "url": "https://geco.amf-france.org/Bio/info_part.aspx?prev=part&NumProd=1872&NumPart=59521"
      }
    ],
    "fund": "OSTRUM ACTIONS SMALL &amp; MID CAP FRANCE",
    "prospectus": "https://geco.amf-france.org/Bio/Bio/BIO_PDFS/NIP_NOTICE_PRODUIT/315119.pdf",
    "family_product": "OPCVM",
    "classification": "Actions fran\u00e7aises",
    "agreement_date": "17/10/1995"
  },...]
"""

import re
from urllib.request import urlopen

from bs4 import BeautifulSoup
from tqdm import tqdm

from prospectus_field_extraction.utils.file_handler import read_json, write_json


def main():
    json_path = 'data/list_of_annotated_fund.json'
    list_of_fund = read_json(json_path)
    list_of_fund = _scrap_information(list_of_fund)
    write_json(list_of_fund, json_path)


def _scrap_information(list_of_fund):
    for fund in tqdm(list_of_fund):
        fund_information = _scrap_fund_information(fund)
        fund.update(fund_information)
        fund = _scrap_share_information(fund)
    return list_of_fund


def _scrap_fund_information(fund):
    num_share = re.search('&NumProd=(.*)&NumPart=', fund['shares'][0]['url']).group(1)
    html = urlopen(f'https://geco.amf-france.org/Bio/info_opcvm.aspx?NumProd={num_share}').read()
    soup = BeautifulSoup(html, features='html.parser')
    table = soup.findAll('table', {'class': 'Tab_Style1'})[0].findAll('tr')
    family_product = table[3].find_all('td', {'class': 'ResultatCritereValue'})[0].text
    classification = table[5].find_all('td', {'class': 'ResultatCritereValue'})[0].text
    agreement_date = table[8].find_all('td', {'class': 'ResultatCritereValue'})[0].text
    fund.update({'family_product': family_product, 'classification': classification, 'agreement_date': agreement_date})
    return fund


def _scrap_share_information(fund):
    for share in fund['shares']:
        if 'isin' not in share:
            continue
        html = urlopen(share['url']).read()
        soup = BeautifulSoup(html, features='html.parser')
        table = soup.findAll('table', {'class': 'Tab_Style1'})[0].findAll('tr')
        try:
            share_category = table[3].find_all('td', {'class': 'ResultatCritereValue'})[0].text
            result_affectation = table[4].find_all('td', {'class': 'ResultatCritereValue'})[0].text
        except IndexError:
            share_category = result_affectation = 'Pas de Valeur liquidative pour cette part'
        share.update({'share_category': share_category, 'result_affectation': result_affectation})
    return fund
