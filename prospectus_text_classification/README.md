# Information extraction

## Scrap documents

NB: You may need to sudo to install `rawjs`
```bash
brew install parallel pup node
brew cask install pdftotext
npm i -g git+https://git@github.com/vbrajon/rawjs.git
parallel --citation
cd data
sh scrap.sh
sh extract.sh
```

#### Prospectus structure

```
Informations clés pour l'investisseur
- Objectifs et politique d'investissement
- Profil de risque et de rendement
- Frais
- Performances passées
- Informations pratiques

Prospectus
- Caractéristiques générales
- Modalités de fonctionnement et de gestion
- Informations d'ordre commercial
- Règles d'investissement
- Risque global
- Règles d’évaluation et de comptabilisation des actifs

Règlement
```

## Train model

Move all annotated CSVs from the webapp to 100m-datascience/prospectus/text_classification/data/app/ and run the training:
```
python train_classification.py -o=model -n=10
```

## Run server

Launch index.html and run:
```
python server.py
```

Test your app on another terminal (or with postman):
```
curl --header "Content-Type: application/json" \
     --request POST \
     --data '{"input":["Frais"]}' \
     http://0.0.0.0:5000/predict
```

Open `index.html` to test the app in your browser.
