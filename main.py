import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import signal

'''
    The goal is to analyze how accurate with different method to calculate walk speed with accerleration-only gryo-only accerleration and gryo
'''


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


def savePlot(df):
    '''
        visualization
    '''
    plt.figure(figsize=(15, 6))
    plt.plot(df['time'], df['acceleration'], label='acceleration')
    plt.plot(df, df['gyro'], label='gyro')
    plt.xlabel('time')
    plt.ylabel('a (m/s^2)')
    plt.legend()
    plt.title('a vs g')
    plt.savefig()


def noiseSmooth(df):
    '''
        use Butterworth filter
    '''
    b, a = signal.butter(3, 0.1, btype='lowpass', analog=False)
    transformed_A = signal.filtfilt(b, a, df['acceleration'])
    transformed_G = signal.filtfilt(b, a, df['gyro'])
    transformed_AG = signal.filtfilt(b, a, df['a_remove_g'])


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


def main():
    data = pd.read_csv(sys.argv[1]).dropna(axis='columns')

    aX = data['ax']
    aX = data['ax']
    aY = data['ay']
    aZ = data['az']

    wX = data['wx']
    wY = data['wy']
    wZ = data['wz']

    time = data['time']
    data['acceleration'] = data.apply(vectorAcceleration, axis=1)
    data['gyro'] = data.apply(vectorGyro, axis=1)
    data['a_remove_g'] = data.apply(gravity_remove, axis=1)
    # output = sys.argv[2]


if __name__ == '__main__':
    main()
