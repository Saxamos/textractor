"""Example of training an additional entity type

This script shows how to add a new entity type to an existing pretrained NER
model. To keep the example short and simple, only four sentences are provided
as examples. In practice, you'll need many more — a few hundred would be a
good start. You will also likely need to mix in examples of other entity
types, which might be obtained by running the entity recognizer over unlabelled
sentences, and adding their annotations to the training set.

The actual training is performed by looping over the examples, and calling
`nlp.entity.update()`. The `update()` method steps through the words of the
input. At each word, it makes a prediction. It then consults the annotations
provided on the GoldParse instance, to see whether it was right. If it was
wrong, it adjusts its weights so that the correct action will score higher
next time.

For more details, see the documentation:
* Training: https://spacy.io/usage/training
* NER: https://spacy.io/usage/linguistic-features#named-entities

Compatible with: spaCy v2.1.0+
Last tested with: v2.1.0
"""
import random
from pathlib import Path

import numpy as np
import spacy
from spacy.util import minibatch, compounding
from tqdm import tqdm

from prospectus_field_extraction import ROOT_PATH
from prospectus_field_extraction.data.script.build_fund_name_dataset import FUND_NAME_LABEL
from prospectus_field_extraction.model.ner import SPLIT_TRAIN
from prospectus_field_extraction.model.ner.test_ner import compute_accuracy
from prospectus_field_extraction.utils.file_handler import read_json


def main(n_iter):
    nlp = _init_model(FUND_NAME_LABEL)
    data = _load_and_balance_data()
    _train_model(nlp, n_iter, data)


def _init_model(new_label):
    random.seed(0)
    nlp = spacy.blank('en')  # can be 'fr'
    ner = nlp.create_pipe('ner')
    nlp.add_pipe(ner)
    ner.add_label(new_label)
    return nlp


def _load_and_balance_data():
    data = [row[1:] for row in read_json(ROOT_PATH / 'data/golden/annotated_data.json')[:SPLIT_TRAIN]]
    # Next line is a filter to balance the data. Chose the right proba between 0 and 1 to get balanced annotated chunks.
    data = [row for row in data if len(row[1]['entities']) > 0 or np.random.rand() > .87]
    is_label = [len(row[1]['entities']) > 0 for row in data]
    print(f'Proportion of chunk with annotations: {sum(is_label) * 100 / len(is_label):.2f}%')
    print(f'Number of training row: {len(data)}')
    return data


def _train_model(nlp, n_iter, training_data):
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']  # disable other pipes during training
    with nlp.disable_pipes(*other_pipes):
        sizes = compounding(1.0, 4.0, 1.001)

        for _ in tqdm(range(n_iter)):
            random.shuffle(training_data)
            batches = minibatch(training_data, size=sizes)
            losses = {}
            for batch in batches:
                texts, annotations = zip(*batch)
                nlp.update(texts, annotations, sgd=nlp.begin_training(), drop=0.35, losses=losses)
            print('Losses', losses)
            accuracy = compute_accuracy(nlp)
            print(f'Accuracy: {accuracy}%')
            _save_model(nlp, f'ckpt_{accuracy}')
    return nlp


def _save_model(nlp, output_dir):
    output_dir = Path(ROOT_PATH / 'model' / 'ner' / output_dir)
    if not output_dir.exists():
        output_dir.mkdir()
    nlp.to_disk(output_dir)
    print('Save model in', output_dir)
