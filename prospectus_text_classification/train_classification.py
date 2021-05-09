import random
from pathlib import Path

import click
import pandas as pd
import spacy
from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score
from spacy.util import minibatch


def load_model(model):
    if model is not None:
        nlp = spacy.load(model)
        print(f'Loaded model {model}')
    else:
        nlp = spacy.blank('fr')
        print('Blank fr model')
    return nlp


def load_classifier(nlp):
    # add the text classifier to the pipeline if it doesn't exist
    # nlp.create_pipe works for built-ins that are registered with spaCy
    if 'textcat' not in nlp.pipe_names:
        textcat = nlp.create_pipe(
            'textcat',
            config={'exclusive_classes': True, 'architecture': 'simple_cnn', }
        )
        nlp.add_pipe(textcat, last=True)
    # otherwise, get it, so we can add labels to it
    else:
        textcat = nlp.get_pipe('textcat')
    return textcat


def save_model(output_dir, nlp, optimizer):
    with nlp.use_params(optimizer.averages):
        nlp.to_disk(output_dir)
    print('Saved model to', output_dir)


def load_data(limit=0, split=0.8):
    """Load data from the IMDB dataset."""
    # Partition off part of the train data for evaluation
    # train_data, _ = thinc.extra.datasets.imdb()
    train_data = pd.read_csv('data/app/dataset.csv')[['text', 'label']].values
    random.shuffle(train_data)
    train_data = train_data[-limit:]
    texts, labels = zip(*train_data)
    all_labels = list(set(labels))
    cats = [{k: y == k for k in all_labels} for y in labels]
    split = int(len(train_data) * split)
    return (texts[:split], cats[:split]), (texts[split:], cats[split:])


def evaluate(tokenizer, textcat, texts, cats):
    docs = (tokenizer(text) for text in texts)
    target = [max(gold, key=lambda k: gold[k]) for gold in cats]
    y = [max(doc.cats, key=lambda k: doc.cats[k]) for i, doc in enumerate(textcat.pipe(docs))]
    labels = ['objectives', 'risk_profile', 'fees', 'past_performance', 'information', 'delete']
    matrix = confusion_matrix(target, y, labels=labels)
    precision = precision_score(target, y, average='micro', labels=labels)
    recall = recall_score(target, y, average='micro', labels=labels)
    f_score = f1_score(target, y, average='micro', labels=labels)
    return {'textcat_p': precision,
            'textcat_r': recall,
            'textcat_f': f_score,
            'confusion_matrix': matrix}


@click.command()
@click.option('-m', '--model', type=str, help='Model name to load.')
@click.option('-o', '--output_dir', type=str, help='Optional output directory.')
@click.option('-n', '--n_iter', type=int, default=20, help='Number of training iterations.')
@click.option('-t2v', '--init_tok2vec', type=Path, is_flag=True, help='Pretrained tok2vec weights.')
def train(model=None, output_dir=None, n_iter=20, n_texts=2000, init_tok2vec=None):
    if output_dir is not None:
        output_dir = Path(output_dir)
        if not output_dir.exists():
            output_dir.mkdir(parents=True)

    nlp = load_model(model)
    textcat = load_classifier(nlp)

    print('Loading data...')
    (train_texts, train_cats), (dev_texts, dev_cats) = load_data()
    print(f'Using {n_texts} examples ({len(train_texts)} training, {len(dev_texts)} evaluation)')
    train_data = list(zip(train_texts, [{'cats': cats} for cats in train_cats]))

    for label in train_cats[0].keys():
        textcat.add_label(label)

    optimizer = nlp.begin_training()
    if init_tok2vec is not None:
        with init_tok2vec.open('rb') as file_:
            textcat.model.tok2vec.from_bytes(file_.read())
    print('Training the model...')
    print('{:^5}\t{:^5}\t{:^5}\t{:^5}'.format('LOSS', 'P', 'R', 'F'))
    batch_sizes = 4
    for i in range(n_iter):
        losses = {}
        # batch up the examples using spaCy's minibatch
        random.shuffle(train_data)
        batches = minibatch(train_data, size=batch_sizes)
        for batch in batches:
            texts, annotations = zip(*batch)
            nlp.update(texts, annotations, sgd=optimizer, drop=0.2, losses=losses)
        with textcat.model.use_params(optimizer.averages):
            # evaluate on the dev data split off in load_data()
            scores = evaluate(nlp.tokenizer, textcat, dev_texts, dev_cats)
        print('{0:.3f}\t{1:.3f}\t{2:.3f}\t{3:.3f}'.format(losses['textcat'], scores['textcat_p'], scores['textcat_r'],
                                                          scores['textcat_f']))

    if output_dir is not None:
        save_model(output_dir, nlp, optimizer)


if __name__ == '__main__':
    train()
