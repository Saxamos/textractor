import re

from prospectus_field_extraction.model.lookup.abstract_finder import lookup_finder

CLASSIFICATION_PATTERNS = ['classification :', 'classification amf :', 'opcvm de classification', 'classification']

LEMMATIZED_CLASSIFICATION_TABLE = {
    'et autre titre de creance international': 'Obligations et/ou titres de créances internationaux',
    'monetaire': 'Fonds monétaires à valeur liquidative variable',
    'et autre titre de creance libelle en euro': 'Obligations et/ou titres de créances libellés en euros',
    'action un pays de l union europeenn': 'Actions des pays de l\'Union Européenne',
    'action un pays de le zone euro': 'Actions de pays de la zone euro',
    'fonds avoir formule': 'Fonds à formule',
    'action francaise': 'Actions françaises',
    'action international': 'Actions internationales',
    'non applicable': 'Sans classification',
    'neer': 'Sans classification',

    # Below are names in official table not yet registered (see: https://geco.amf-france.org/Bio/rech_part.aspx)
    # Garanti ou assorti d'une protection
    # FPCI-SICAV
    # Fonds monétaires à valeur liquidative constante de dette publique
    # Fonds monétaires à valeur liquidative à faible volatilité
    # Fonds Immobilier
    # Fonds commun de placement à innovation
    # Fonds commun à risques
    # Fonds d'investissement de proximité
    # Fonds commun d’investissement sur les marchés à terme
    # Fonds de multigestion alternative

    # Below are names not in official table (see: https://geco.amf-france.org/Bio/rech_part.aspx)
    'opc d opc': 'OPC d\'OPC',
    'mixte': 'Mixte',
    'action': 'Actions',
}

LOOKUP_CLASSIFICATION_TABLE = {k: 0 for k in LEMMATIZED_CLASSIFICATION_TABLE.keys()}


def find_classification_pattern(text):
    for field_pattern in CLASSIFICATION_PATTERNS:
        for el in re.finditer(field_pattern, text):
            return text[el.start():el.end() + 100]


def main():
    lookup_finder(LOOKUP_CLASSIFICATION_TABLE, LEMMATIZED_CLASSIFICATION_TABLE, find_classification_pattern)
