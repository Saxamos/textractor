import base64

import pdftotext
import spacy
import streamlit as st

from prospectus_field_extraction import ROOT_PATH
from prospectus_field_extraction.model.lookup.benchmark_finder import LEMMATIZED_BENCHMARK_TABLE, find_benchmark_pattern
from prospectus_field_extraction.model.lookup.classification_finder import (LOOKUP_CLASSIFICATION_TABLE,
                                                                            find_classification_pattern,
                                                                            LEMMATIZED_CLASSIFICATION_TABLE)
from prospectus_field_extraction.model.lookup.closing_date_finder import (LEMMATIZED_CLOSING_DATE_TABLE,
                                                                          find_closing_date_pattern)
from prospectus_field_extraction.model.lookup.depositary_finder import (LOOKUP_DEPOSITARY_TABLE,
                                                                        LEMMATIZED_DEPOSITARY_TABLE,
                                                                        find_depositary_pattern)
from prospectus_field_extraction.model.lookup.goal_finder import LEMMATIZED_GOAL_TABLE, find_goal_pattern
from prospectus_field_extraction.model.lookup.inception_date_finder import (find_inception_date_pattern,
                                                                            LEMMATIZED_INCEPTION_DATE_TABLE)
from prospectus_field_extraction.model.lookup.isin_finder import find_isin_pattern, LEMMATIZED_ISIN_TABLE
from prospectus_field_extraction.utils.aggregater import compute_count_sorted_dict
from prospectus_field_extraction.utils.file_handler import clean_text


def main():
    st.title('Extracteur d\'information de prospectus')
    ner_model, fr_lemmatizer = _load_models()
    tables = _build_tables()

    pdf_file = st.file_uploader('', type=['pdf'])
    show_file = st.empty()
    if not pdf_file:
        show_file.info('Sélectionnez un PDF de prospectus à traiter.')
        return

    pdf_display = _build_pdf_display(pdf_file)
    st.markdown(pdf_display, unsafe_allow_html=True)

    pdf_text = _convert_pdf_to_text_and_clean(pdf_file)

    name = _run_ner_model(pdf_text, ner_model)
    lookup_predictions = _run_lookup_model(pdf_text, fr_lemmatizer, tables)

    prediction_display = _build_prediction_display(name, **lookup_predictions)
    show_file.info(prediction_display)
    pdf_file.close()


@st.cache(allow_output_mutation=True)
def _load_models():
    ner_model = spacy.load(ROOT_PATH / 'app' / 'ner_production_model')
    fr_lemmatizer = spacy.load('fr_core_news_md')
    print('Models Loaded.')
    return ner_model, fr_lemmatizer


@st.cache(allow_output_mutation=True)
def _build_tables():
    return {
        'isin': ({}, LEMMATIZED_ISIN_TABLE, find_isin_pattern),
        'classification': (LOOKUP_CLASSIFICATION_TABLE, LEMMATIZED_CLASSIFICATION_TABLE, find_classification_pattern),
        'depositary': (LOOKUP_DEPOSITARY_TABLE, LEMMATIZED_DEPOSITARY_TABLE, find_depositary_pattern),
        'benchmark': ({}, LEMMATIZED_BENCHMARK_TABLE, find_benchmark_pattern),
        'goal': ({}, LEMMATIZED_GOAL_TABLE, find_goal_pattern),
        'inception_date': ({}, LEMMATIZED_INCEPTION_DATE_TABLE, find_inception_date_pattern),
        'closing_date': ({}, LEMMATIZED_CLOSING_DATE_TABLE, find_closing_date_pattern),
    }


def _build_pdf_display(pdf_file):
    base64_pdf = base64.b64encode(pdf_file.read()).decode('utf-8')
    return f'<embed src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf">'


def _convert_pdf_to_text_and_clean(pdf_file):
    pdf_file.seek(0)
    pdf_text = pdftotext.PDF(pdf_file)
    return clean_text('\n\n'.join(pdf_text))


def _run_ner_model(text, ner_model):
    chunked_text = [chunk for chunk in text.split('\n\n')]
    predictions = [pred.text for chunk in chunked_text for pred in ner_model(chunk).ents]
    pred_count_sorted_dict = compute_count_sorted_dict(predictions)
    try:
        best_pred = list(pred_count_sorted_dict.keys())[0]
    except IndexError:
        best_pred = 'Non trouvé'
    return best_pred


def _run_lookup_model(text, fr_lemmatizer, tables):
    predictions = {}
    for key, (lookup_table, lemmatized_table, find_pattern_func) in tables.items():
        pattern = find_pattern_func(text)
        if type(pattern) == set:
            predictions[key] = ', '.join(pattern)
            continue
        elif not pattern:
            predictions[key] = lemmatized_table['neer']
        elif len(lookup_table) == 0:
            predictions[key] = pattern
        else:
            lemmatized_pattern = ' '.join([token.lemma_ for token in fr_lemmatizer(pattern)])
            for field in lookup_table.keys():
                if field in lemmatized_pattern:
                    predictions[key] = lemmatized_table[field]
                    break
        if key not in predictions:
            predictions[key] = lemmatized_table['neer']

    return predictions


def _build_prediction_display(name, isin, classification, depositary, benchmark, goal, inception_date, closing_date):
    return f"""
**Nom du fond** : {name}

**Liste d'ISIN** : {isin}

**Classification** : {classification}

**Dépositaire** : {depositary}

**Indicateur de référence** : {benchmark}

**Date de création** : {inception_date}

**Date de clôture** : {closing_date}

**Objectif de gestion** : {goal}
"""


if __name__ == '__main__':
    main()
