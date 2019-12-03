import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal, integrate

walk_foot = pd.read_csv('data/walk_foot-2019-11-2715.42.22.csv').dropna(axis='columns')
run_foot = pd.read_csv('data/run_foot-2019-11-2715.55.43.csv').dropna(axis='columns')
upstairs_foot = pd.read_csv('data/upstairs_foot-2019-11-2715.23.25.csv').dropna(axis='columns')
downstairs_foot = pd.read_csv('data/downstairs_foot-2019-11-2715.23.59.csv').dropna(axis='columns')

activity_type = [walk_foot, run_foot, upstairs_foot, downstairs_foot]
vel = []
def vectorAcceleration(df):
    '''
        calculate vector acceleration
    '''
    return np.sqrt(df['ax_filtered']**2 + df['ay_filtered']**2 + df['az_filtered']**2)

def noiseSmooth(df):
    '''
        use Butterworth filter
    '''
    b, a = signal.butter(3, 0.05, btype='lowpass', analog=False)
    df['ax_filtered'] = signal.filtfilt(b, a, df['ax'])
    df['ay_filtered'] = signal.filtfilt(b, a, df['ay'])
    df['az_filtered'] = signal.filtfilt(b, a,  df['az'])
    return df

def vel_integration(acc_lst, time_lst):
    acc = np.array(acc_lst, dtype=np.float64)
    vel = integrate.cumtrapz(acc, time_lst, initial=0)
#     dist = integrate.cumtrapz(vel, time, initial=0)
    return vel

def extractData(df, min=5, max=15):
    '''
    extrac start and beginning dummy data
    '''
    return df.iloc[5000:10000].reset_index(drop=True)

for i, m in enumerate(activity_type):  # yes, you can leave this loop in if you want.
    m =extractData(m)
    m = noiseSmooth(m)
    m['magnitude_acc'] = m.apply(vectorAcceleration, axis=1)
    vel_acc_filtered = vel_integration(m.magnitude_acc, m.time)
    vel.append(vel_acc_filtered)


df2 = walk_foot.iloc[5000:10000]
x2 = df2['time']
plt.plot(x2, vel[0], label='walk')
plt.plot(x2, vel[1], label='run')
plt.plot(x2, vel[2], label='upstairs')
plt.plot(x2, vel[3], label='downstairs')
plt.legend()
plt.savefig(f'./fig/velocity.png')