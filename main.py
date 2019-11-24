import sys
from glob import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import signal
from scipy.signal import find_peaks_cwt


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


def getLocalMaximum(df):
    indexes = find_peaks_cwt(df['g_removed'], np.arange(1, 550))
    # plt.plot(df['a_remove_g'])
    # plt.plot(indexes, df['a_remove_g'][indexes], "x")
    # plt.plot(np.zeros_like(df['a_remove_g']), "--", color="gray")
    # plt.show()


def main():
    data = pd.read_csv(sys.argv[1]).dropna(axis='columns')


if __name__ == '__main__':
    main()
