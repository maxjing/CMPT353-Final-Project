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

path_re = re.compile(r"^(.+/)([^-]*)")
type_re = re.compile(r"(.+)_")


def extractFileName(path):
    '''
    extract file name from file path
    '''
    m = path_re.match(path)
    return m.group(2)


def extractTypeName(path):
    '''
    extract label
    '''
    m = type_re.match(path)
    return m.group(1)


def extractData(df, min=5, max=15):
    '''
    extrac start and beginning dummy data
    '''
    condition = (df['time'] > min) & (df['time'] < max)
    return df.loc[condition].reset_index(drop=True)


def noiseSmooth(df):
    '''
        use Butterworth filter
    '''
    b, a = signal.butter(3, 0.05, btype='lowpass', analog=False)
    df['ax_filtered'] = signal.filtfilt(b, a, df['ax'])
    df['ay_filtered'] = signal.filtfilt(b, a, df['ay'])
    df['az_filtered'] = signal.filtfilt(b, a,  df['az'])
    df['wx_filtered'] = signal.filtfilt(b, a, df['wx'])
    df['wy_filtered'] = signal.filtfilt(b, a, df['wy'])
    df['wz_filtered'] = signal.filtfilt(b, a,  df['wz'])
    return df


def main():
    os.mkdir(csv_folder)
    dtypes1 = ['float', 'float', 'float', 'float', 'float', 'float',
               'float', 'float', 'float', 'float', 'float', 'float', 'float', 'str']
    dtypes2 = ['float', 'float', 'float', 'float', 'float', 'float', 'float']
    for f in files:
        fileName = extractFileName(f)
        typeName = extractTypeName(fileName)
        df = pd.read_csv(f).dropna(axis='columns')
        df = extractData(df)
        df = noiseSmooth(df)
        df['label'] = typeName
        df = df.drop(columns='time')
        df.to_csv(os.path.join(
            f'{root_dir}/{csv_folder}/{fileName}.csv'), mode='a', index=False, header=False)


if __name__ == '__main__':
    main()
