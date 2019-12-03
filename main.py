import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import FunctionTransformer
from skimage.color import rgb2lab
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier

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

def train_model(df):
    X = df[SENSOR_DATA_COLUMNS].values
    y = df['label'].values

    X_train, X_valid, y_train, y_valid = train_test_split(X, y)

    bayes_model = GaussianNB()

    knn_model = KNeighborsClassifier(n_neighbors=5)

    rf_model = RandomForestClassifier(n_estimators=100, max_depth=10, min_samples_leaf=10)

    models = [bayes_model, knn_model, rf_model]
    for i, m in enumerate(models):
        m.fit(X_train, y_train)
        
    OUTPUT_TEMPLATE = (
        'Bayesian classifier:    {bayes_rgb:.3f} \n'
        'kNN classifier:         {knn_rgb:.3f} \n'
        'Rand forest classifier: {rf_rgb:.3f} \n'
    )
    print(OUTPUT_TEMPLATE.format(
        bayes_rgb=bayes_model.score(X_valid, y_valid),
        knn_rgb=knn_model.score(X_valid, y_valid),
        rf_rgb=rf_model.score(X_valid, y_valid),
    ))

def main():
    # create_plots()
    foot_combined = pd.concat([walk_foot, run_foot, upstairs_foot, downstairs_foot]).reset_index()
    pocket_combined = pd.concat([walk_pocket, run_pocket, upstairs_pocket, downstairs_pocket]).reset_index()
    hand_combined = pd.concat([walk_hand, run_hand, upstairs_hand, downstairs_hand]).reset_index()
    train_model(foot_combined)
    train_model(pocket_combined)
    train_model(hand_combined)

if __name__ == '__main__':
    main()
