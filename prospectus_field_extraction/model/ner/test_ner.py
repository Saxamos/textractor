from collections import defaultdict

import spacy
from Levenshtein import distance
from tqdm import tqdm

from prospectus_field_extraction import ROOT_PATH
from prospectus_field_extraction.model.ner import SPLIT_TRAIN, SPLIT_TEST
from prospectus_field_extraction.utils.file_handler import read_json


def main(model, verbose):
    if verbose < 2:
        print('Loading:', model)
    print('found///gt///prediction///proba_dict')
    nlp = spacy.load(ROOT_PATH / 'model' / 'ner' / model)
    accuracy = compute_accuracy(nlp, verbose=verbose)
    if verbose < 2:
        print(f'Accuracy: {accuracy}%')


def compute_accuracy(nlp, verbose=0):
    founds = []
    data = read_json(ROOT_PATH / 'data/golden/annotated_data.json')[SPLIT_TRAIN:SPLIT_TEST]
    files = set([prospectus[0] for prospectus in data])
    if verbose > 0:
        files = tqdm(files)
    for file in files:
        annotated_data_one_prospectus = [el[1:] for el in data if el[0] == file]

        gt = _compute_ground_truth(annotated_data_one_prospectus)
        if not gt:
            if verbose is 1:
                print(f'NO GROUND TRUTH FOUND IN PROSPECTUS: {file}')
            continue

        proba_dict = _predict_proba(annotated_data_one_prospectus, nlp)
        prediction = _compute_prediction(proba_dict)

        found = True if (distance(prediction, gt) < 6 or gt in prediction or prediction in gt) and prediction else False
        if verbose > 0:
            print(f'{found}///{gt}///{prediction}///{proba_dict}')
        founds.append(found)
    return round(sum(founds) * 100 / len(founds), 2)


def _predict_proba(annotated_data_one_prospectus, nlp):
    proba_dict = defaultdict(list)
    for text, _ in annotated_data_one_prospectus:
        doc = nlp(text)
        beams = nlp.entity.beam_parse([doc], beam_width=16, beam_density=0.0001)
        for beam in beams:
            for score, ents in nlp.entity.moves.get_beam_parses(beam):
                for start, end, label in ents:
                    proba_dict[doc[start:end].text].append(round(score, 3))
    return dict(proba_dict)


def _compute_prediction(proba_dict):
    sum_proba_dict = {k: sum(v) for k, v in proba_dict.items()}
    sum_proba_sorted_dict = {k: v for k, v in sorted(sum_proba_dict.items(), key=lambda item: item[1], reverse=True)}
    try:
        return list(sum_proba_sorted_dict.keys())[0]
    except IndexError:
        return ''


def _compute_ground_truth(annotated_data_one_prospectus):
    gt = ''
    for annotation in annotated_data_one_prospectus:
        gt_index = annotation[1]['entities']
        if len(gt_index) > 0:
            gt = annotation[0][gt_index[0][0]:gt_index[0][1]]
            break
    return gt
