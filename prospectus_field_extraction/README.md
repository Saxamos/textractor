# Information extraction


## Usage

### Setup env

NB: Make sure to have `python3` and `pip3` by default
NB: You may need to sudo to install `rawjs`
```bash
brew install parallel pup node poppler
brew cask install pdftotext
sudo npm i -g git+https://git@github.com/vbrajon/rawjs.git
parallel --citation
pip install -r requirements.txt
pip install -e .
```

### CLI

To get all the possible commmand, run:
```bash
prospectus --help
```

- `prospectus download`: Scrap list of fund with associated information, download PDFs prospectus and preprocess data.
- `prospectus lookup <field_name>`: Run the test script for the lookup model in order to enhance it.
- `prospectus ner <mode>`:
    - `prospectus ner train --n-iter-train=20`: Train the NER model.
    - `prospectus ner test --model-dir-test=<dir> --verbosity-test=2 > prospectus_field_extraction/model/ner/result.csv`
    : Test NER model and save results.
- `prospectus app`: Launch the streamlit application.

### Deploy on heroku

```bash
git push heroku <branch-name>:master
```
Find the app running here: https://prospectus-extractor.herokuapp.com/

### Train new model

- NER

In order to train a new NER model, the most diffcult part is to create the annotated dataset
 (see "Dataset & annotation for NER model" paragraph for more information).

You can either chose to train a specific model for this label or you can train a multi-label model. Be aware that
 for multi-label model you can have difficulties (e.g. when there is a label collision in a bunch of token). 

- Lookup

For the Lookup model, read carefully the [abstract code](model/lookup/abstract_finder.py).
It will give you hints on how to implement the new field search. The idea is basically to create the following tables:

    - LOOKUP_<field_name>_TABLE
    - LEMMATIZED_<field_name>_TABLE
    - find_<field_name>_pattern

Don't hesistate to get inspired from the existing finders.
Also add the new field in the [entry point](__main__.py) to be able to run the script.

In both case, when the accuracy seems reasonably good, you can integrate the new model in the
 [streamlit app](app/streamlit_app.py) with respect to the existing design. 

### Run the test

To run all the tests please launch:
```
python -m pytest
```

## Data

### Information to extract

- NER model
    - nom du fond (NER accuracy 82.94%)
- LOOKUP model
    - dépositaire (Lookup Accuracy: 95.49%)
    - classification (Lookup Accuracy: 74.48%)
    - nom du benchmark (Lookup Accuracy: 77.26%)
    - objectif de gestion (Lookup Accuracy: 96.76%)
    - isin + nom des parts (Lookup Accuracy: 100%)
    - date d'inception (Lookup Accuracy: 98.00%)
    - date de clôture (Lookup Accuracy: 94.79%)
- OBJECT_DETECTION model
    - échelle de risque (to be implemented)
- Not yet implemeneted
    - frais (entrée, sortie, courants, commission de performance)
    - méthode de calcul du risque global
    - type de fonds (not relevant => only OPCVM here)

### Dataset & annotation for NER model

```
TRAIN_DATA = [
    ("Horses and cats are too tall.", {"entities": [(0, 6, "ANIMAL"), (11, 15, "ANIMAL")]}),
    ("Do they bite?", {"entities": []}),
    ("horses?", {"entities": [(0, 6, "ANIMAL")]}),
]
```


## Documentation

You can find the french documentation
 [here](https://docs.google.com/document/d/1sZiHgCI4SMMQR4ls-vbAwVrGzcaM5TC3aLq3iy4py4M/edit?usp=sharing) for the 
 IA project (model, hypothesis and results)


## TODO

#### Model
- Use prodigy to annotate new labels (https://prodi.gy/docs)
- Search minimal number of annotation that gives good results (several training with different training database size)
- Train NER with another label (e.g. benchmark)
- (Improve NER model by blending with another model (e.g. huggingface or allennlp) when confidence is low)
- Blend NER & LOOKUP
- Use more data (other than OPCVM) 
- Weight pdf with error
- Improve Lookup model with more pattern
- Implement object detection for risk field
#### Pipeline
- Log automatically model hyperparameters in the `nlp` object (dataset, cv, n_iter, language, data balancing)
- (Update automatically computed score in README)
- Make clean implementation from code in `sandbox` folder
#### App
- Change heroku to Zeit to be iso with other projects
- Test the code and separate streamlit code from our function
- Enhance render in front for certain field (e.g. remove lemmatization by adding ponctuation)
- Add new page app with video demo & model explanation
- Implement last fields: (risque, frais, méthode de calcul et type de fond)
- Highlight found fields in PDF
