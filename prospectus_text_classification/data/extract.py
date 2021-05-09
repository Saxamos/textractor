import glob
import os

import pandas as pd

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))

files = glob.glob(os.path.join(ROOT_PATH, 'raw', '*.txt'))
all_files = []
for file in files:
    with open(file, 'r+') as f:
        try:
            lines = f.readlines()
        except Exception as e:
            print('error', file)
            continue
    df = pd.DataFrame([x.strip() for x in lines])
    df = df[df[0].str.len() > 20].assign(file=file)
    all_files.append(df)

all_df = pd.concat(all_files).rename(columns={0: 'text'})
all_df.to_csv(os.path.join(ROOT_PATH, 'golden', 'prospectus.csv'), index=False, encoding='utf-8-sig')
