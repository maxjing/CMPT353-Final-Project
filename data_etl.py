import sys
import os
from glob import glob
import pandas as pd
import numpy as np
from scipy import signal

root_dir = os.path.abspath(os.path.dirname(sys.argv[0]) or '.')
csv_folder = 'data_processed'


def vectorAcceleration(df):
    '''
        calculate vector acceleration
    '''
    return np.sqrt(df['ax']**2 + df['ay']**2 + df['az']**2)


def vectorGyro(df):
    '''
        calculate vector gravity acceleration
    '''
    return np.sqrt(df['wx']**2 + df['wy']**2 + df['wz']**2)


def gravity_remove(df):
    '''
        remove gravity compensate from accerlermeter 
        method inspired by android official document
        https://developer.android.com/reference/android/hardware/SensorEvent.html
    '''
    alpha = 0.6
    l = [0.0, 0.0, 0.0]
    g = [0.0, 0.0, 0.0]
    g[0] = alpha * df['wx'] + (1 - alpha) * df['ax']
    g[1] = alpha * df['wy'] + (1 - alpha) * df['ay']
    g[2] = alpha * df['wz'] + (1 - alpha) * df['az']

    l[0] = df['ax'] - g[0]
    l[1] = df['ay'] - g[1]
    l[2] = df['az'] - g[2]
    return np.sqrt(l[0]**2 + l[1]**2 + l[2]**2)


def create_csv(df, category, i):
    df.to_csv(os.path.join(f'{root_dir}/{csv_folder}/{category}-{i}.csv'), index=False)


def noiseSmooth(df):
    '''
        use Butterworth filter
    '''
    b, a = signal.butter(3, 0.05, btype='lowpass', analog=False)
    df['acceleration'] = signal.filtfilt(b, a, df['acceleration'])
    df['gyro'] = signal.filtfilt(b, a, df['gyro'])
    df['g_removed'] = signal.filtfilt(b, a,  df['g_removed'])


def process_category_data(dfs, category):
    '''
        calculate vector accelerations and smooth the data
    '''
    b, a = signal.butter(3, 0.05, btype='lowpass', analog=False)
    for i in range(len(dfs)):
        df = pd.DataFrame(columns=['time', 'acceleration', 'gyro', 'g_removed'])
        df['time'] = dfs[i]['time']
        df['acceleration'] = dfs[i].apply(vectorAcceleration, axis=1)
        df['gyro'] = dfs[i].apply(vectorGyro, axis=1)
        df['g_removed'] = dfs[i].apply(gravity_remove, axis=1)
        df = df[['time', 'acceleration', 'gyro', 'g_removed']]
        noiseSmooth(df)
        create_csv(df, category, i+1)


def main():
    walk_filenames = glob('./data/walk*.csv')
    walk = [pd.read_csv(f).dropna(axis='columns') for f in walk_filenames]
    run_filenames = glob('./data/run*.csv')
    run = [pd.read_csv(f).dropna(axis='columns') for f in run_filenames]
    climb_stairs_filenames = glob('./data/climb_stairs*.csv')
    climb_stairs = [pd.read_csv(f).dropna(axis='columns') for f in climb_stairs_filenames]

    process_category_data(walk, 'walk')
    process_category_data(run, 'run')
    process_category_data(climb_stairs, 'climb_stairs')


if __name__ == '__main__':
    main()
