import pandas as pd


def main():
    save_bbg_data()


def clean_datas(securities, columns):
    bbg_df = pd.DataFrame(data=securities, columns=columns)
    # nettoyer le champs ISIN
    bbg_df["SECURITIES"] = bbg_df["SECURITIES"].str.split(" ", expand=True)[0]
    # supprimer la dernière colonne inutile
    bbg_df = bbg_df.drop(labels='\n', axis=1)
    return bbg_df


def save_as_json(bbg_df):
    bbg_json = bbg_df.to_json(orient="records")
    with open('../data/bbg_datas.json', 'w') as f:
        f.write(bbg_json)


def save_bbg_data():
    # ouvrir l'extraction bbg
    with open("../data/BBG_FundU201912101124_dec.out", "r") as f:
        lines = f.readlines()

    # definir la ligne des noms de colonne
    COLUMN_LINE = 100
    columns = lines[COLUMN_LINE].split("|")

    # définir la ligne de début des données
    START_LINE = 102
    securities = []

    # recupérer les données sur les fonds
    for START_LINE in range(START_LINE, len(lines) - 3, 2):
        securities.append(lines[START_LINE].split("|"))

    # nettoyer les données des fonds
    bbg_df = clean_datas(securities, columns)
    # sauver les données au format JSON
    save_as_json(bbg_df)


if __name__ == '__main__':
    main()
