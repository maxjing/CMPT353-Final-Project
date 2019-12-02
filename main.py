import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
cols = ['ax', 'ay', 'az', 'wx', 'wy', 'wz', 'ax_filtered', 'ay_filtered',
        'az_filtered', 'wx_filtered', 'wy_filtered', 'wz_filtered', 'label']

SENSOR_DATA_COLUMNS = ['ax_filtered', 'ay_filtered',
                       'az_filtered', 'wx_filtered', 'wy_filtered', 'wz_filtered']

walk_foot = pd.read_csv('data_processed/walk_foot.csv', names=cols)
run_foot = pd.read_csv('data_processed/run_foot.csv', names=cols)
upstairs_foot = pd.read_csv('data_processed/upstairs_foot.csv', names=cols)
downstairs_foot = pd.read_csv('data_processed/downstairs_foot.csv', names=cols)

walk_pocket = pd.read_csv('data_processed/walk_pocket.csv', names=cols)
run_pocket = pd.read_csv('data_processed/run_pocket.csv', names=cols)
upstairs_pocket = pd.read_csv('data_processed/upstairs_pocket.csv', names=cols)
downstairs_pocket = pd.read_csv('data_processed/downstairs_pocket.csv', names=cols)

walk_hand = pd.read_csv('data_processed/walk_hand.csv', names=cols)
run_hand = pd.read_csv('data_processed/run_hand.csv', names=cols)
upstairs_hand = pd.read_csv('data_processed/upstairs_hand.csv', names=cols)
downstairs_hand = pd.read_csv('data_processed/downstairs_hand.csv', names=cols)


def create_plots():
    os.mkdir('fig')
    for c in SENSOR_DATA_COLUMNS:
        plt.figure(figsize=(5, 5))
        plt.title('Foot')
        sns.distplot(walk_foot[c], label='walk')
        sns.distplot(run_foot[c], label='run')
        sns.distplot(upstairs_foot[c], label='upstairs')
        sns.distplot(downstairs_foot[c], label='downstairs')
        plt.legend()
        plt.savefig(f'./fig/foot-{c}.png')
    for c in SENSOR_DATA_COLUMNS:
        plt.figure(figsize=(5, 5))
        plt.title('Hand')
        sns.distplot(walk_hand[c], label='walk')
        sns.distplot(run_hand[c], label='run')
        sns.distplot(upstairs_hand[c], label='upstairs')
        sns.distplot(downstairs_hand[c], label='downstairs')
        plt.legend()
        plt.savefig(f'./fig/hand-{c}.png')
    for c in SENSOR_DATA_COLUMNS:
        plt.figure(figsize=(5, 5))
        plt.title('Pocket')
        sns.distplot(walk_pocket[c], label='walk')
        sns.distplot(run_pocket[c], label='run')
        sns.distplot(upstairs_pocket[c], label='upstairs')
        sns.distplot(downstairs_pocket[c], label='downstairs')
        plt.legend()
        plt.savefig(f'./fig/pocket-{c}.png')


def main():
    create_plots()


if __name__ == '__main__':
    main()
