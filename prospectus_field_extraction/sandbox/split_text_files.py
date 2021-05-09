import os

from prospectus_field_extraction.utils.file_handler import read_json

START_KID_KEYWORDS = ['Informations Clés pour l’Investisseur', 'Informations clés pour l\'investisseur',
                      'INFORMATIONS CLES POUR L’INVESTISSEUR', 'INFORMATIONS CLES POUR L\'INVESTISSEUR',
                      'NFORMATIONS CLES POUR L’INVESTISSEUR', 'INFORMATIONS CLES\nPOUR LES INVESTISSEURS',
                      'Information clé pour l\'investisseur', 'Information Clés pour l’Investisseur',
                      'Information clé pour l’investisseur', 'Informations clés\npour l’investisseur',
                      'INFORMATION CLE POUR\nL’INVESTISSEUR']

END_KID_KEYWORDS = ['Informations Clés pour l’Investisseur', 'Informations clés pour l\'investisseur',
                    'INFORMATIONS CLES POUR L’INVESTISSEUR', 'INFORMATIONS CLES POUR L\'INVESTISSEUR',
                    'NFORMATIONS CLES POUR L’INVESTISSEUR', 'INFORMATIONS CLES\nPOUR LES INVESTISSEURS',
                    'Information clé pour l\'investisseur', 'Information Clés pour l’Investisseur',
                    'Informations clés\npour l’investisseur', 'Information clé pour l’investisseur',
                    'INFORMATION CLE POUR\nL’INVESTISSEUR',
                    'OPCVM relevant de la directive 2009/65/CE']


def is_start_keyword_in(page):
    # recherche un mot clé indiquant le début du kid dans la première moitié de la page
    for word in START_KID_KEYWORDS:
        mid_page = int(len(page) / 2)
        if word.lower() in page[:mid_page].lower():
            return True


def is_end_keyword_in(page):
    # recherche un mot clé indiquant la fin du kid
    for word in END_KID_KEYWORDS:
        if word.lower() in page.lower():
            return True


def main():
    files = build_file_list()

    file_nb = len(files)
    missing_kid = 0
    nb_kid = 0

    for file in files:
        file_name = '../data/raw/' + file
        if os.path.isfile(file_name):
            with open(file_name, encoding='utf-8') as f:
                text = f.read()
                pages = text.split('\f')
                kid = []
                kid_count = 0
                for page in pages:
                    # on ajoute la page si mot clé début
                    if is_start_keyword_in(page) and not kid:
                        kid.append(page + '\f')
                    # on sauve les pages dans un fichier si mot clé fin
                    elif is_end_keyword_in(page) and kid:
                        kid_count = kid_count + 1
                        new_file_name = os.path.splitext(file)[0] + "_" + str(kid_count) + ".txt"
                        with open('../data/raw/kids/' + new_file_name, 'w') as f:
                            for kid_page in kid:
                                f.write("%s\n" % kid_page)
                        kid = []
                        # et on ajoute la page si elle contient un mot clé début aussi
                        if is_start_keyword_in(page):
                            kid.append(page + '\f')
                    # on ajoute la page si il y en a déjà au moins 1
                    elif kid:
                        kid.append(page + '\f')

                # on compte le nombre de fichiers ayant un kid et ceux n'ayant pas de kid
                if kid_count == 0:
                    missing_kid = missing_kid + 1
                    # on liste les fichiers n'ayant pas de kid
                    print(file)
                else:
                    nb_kid = nb_kid + 1

    print("nombre de fichiers analysés :" + str(file_nb))
    print("nombre de fichiers contenant au moins 1 kid :" + str(nb_kid))
    print("nombre de fichiers manquants: " + str(missing_kid))


def build_file_list():
    json_data = read_json('data/list_of_annotated_fund.json')
    files = []
    for data in json_data:
        files.append(data['prospectus'].split('/')[-1].replace('pdf', 'txt'))
    return files


if __name__ == '__main__':
    main()
