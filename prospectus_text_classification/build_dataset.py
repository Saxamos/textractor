import glob
import os

import pandas as pd

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
APP_DIR = os.path.join(ROOT_PATH, 'data', 'app')

files = glob.glob(os.path.join(APP_DIR, '*annotated.csv'))

all_text = []
for file in files:
    print(file)
    df = pd.read_csv(file)
    all_text.append(df.dropna())

pd.concat(all_text).to_csv(os.path.join(APP_DIR, 'dataset.csv'), index=False)
