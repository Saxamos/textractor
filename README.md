# textractor

## Projects

#### Prospectus
The goal of this project is to extract specific financial information from AMF prospectus pdf.
It is splitted in two step: text classification and field extraction.

[Contribution guidelines for classification project](prospectus_text_classification/README.md)

[Contribution guidelines for extraction project](prospectus_field_extraction/README.md)


## Workflow

#### AI
1. Define task
2. Find data
3. Annotate data
4. Run baseline model
    1. Annotate a small dataset
    2. Run on small dataset
5. Improve model
6. Deploy

#### Data management
1. Extract raw data in folder `data/raw/`
2. Transform data in folder `data/golden/`
3. Load data from folder `data/app/`

## Repo organisation

In each project, the models should be stored in `model/`.

The data should be in `data/` with the ETL structure as explain above.
