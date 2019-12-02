import sys
import os
from glob import glob
import pandas as pd
import numpy as np
from scipy import signal
import re

root_dir = os.path.abspath(os.path.dirname(sys.argv[0]) or '.')
csv_folder = 'data_processed'
files = glob('./data/*.csv')

labels = ['walk', 'run', 'upstairs', 'downstairs']
positions = ['foot', 'hand', 'pocket']
observers = ['ax', 'ay', 'az', 'wx', 'wy', 'wz']

path_re = re.compile(r"^(.+/)([^-]*)")
type_re = re.compile(r"(.+)_")


def extractFileName(path):
    '''
    extract file name from file path
    '''
    m = path_re.match(path)
    return m.group(2)


def extractTypeName(path):
    m = type_re.match(path)
    return m.group(1)


def extractData(df, min=5, max=15):
    '''
    extrac start and beginning dummy data
    '''
    condition = (df['time'] > min) & (df['time'] < max)
    return df.loc[condition].reset_index(drop=True)


def main():
    os.mkdir(csv_folder)
    for f in files:
        fileName = extractFileName(f)
        typeName = extractTypeName(fileName)
        original_df = pd.read_csv(f).dropna(axis='columns')
        original_df = extractData(original_df)
        original_df['label'] = typeName
        original_df.to_csv(os.path.join(
            f'{root_dir}/{csv_folder}/{fileName}.csv'), mode='a')
        for observer in observers:
            df = pd.DataFrame()
            df[observer] = original_df[observer]
            df.to_csv(os.path.join(
                f'{root_dir}/{csv_folder}/{fileName}-{observer}.csv'), mode='a', header=False, index=False)


if __name__ == '__main__':
    main()
