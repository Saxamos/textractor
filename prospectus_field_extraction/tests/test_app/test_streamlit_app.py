import spacy

from prospectus_field_extraction.app.streamlit_app import _run_lookup_model, _build_tables


def test_run_lookup_model():
    # Given
    text = 'un faux text pdf en francais prealablement nettoye'
    fr_lemmatizer = spacy.load('fr_core_news_md')
    tables = _build_tables()

    # When
    predictions = _run_lookup_model(text, fr_lemmatizer, tables)

    # Then
    expected = {'isin': '',
                'classification': 'Sans classification',
                'depositary': 'Sans dépositaire',
                'benchmark': "Pas d'indicateur de référence",
                'goal': 'Non trouvé',
                'inception_date': 'Non trouvé',
                'closing_date': 'Non trouvé'}
    assert predictions == expected
