# cmpt353-group-cj

## requrired library
*Pandas
*Numpy
*Matplotlib
*SciPy
*Seaborn
*re
*scikit-learn

## data
1. put csv data into /data folder
    rule: filename start with categories including ['walk', 'run', 'upstairs', 'downstairs'] with method ['pocket', 'hand', 'foot']

## steps:
1. run `python3 data_etl.py`
    
    This will produce `data_processed` folder with combined and filtered data

    Filenames start with categories including ['walk', 'run', 'upstairs', 'downstairs'] with location ['pocket', 'hand', 'foot']

2. run `python3 main.py`

    This script will create a new folder called `fig` which will contain 18 distribution graph of ax, ay, az, wx, wy, wz from different locations

3. (optional) run `python3 velocity.py`
    
    This will create three graphs of velocity calculated from walk_foot filtered_ax, filtered_ay and magnitude_acc = sqrt(df['ax_filtered']**2 + df['ay_filtered']**2 + df['az_filtered']**2)