import pandas as pd
import numpy as np
import regex as re

# import data
df = pd.read_csv('h216.csv')
household_cols = pd.read_csv('household_columns.csv')
household_cols_clean = pd.read_csv('household_columns_clean.csv')

# create dict for column  names and description
col_dict = {}
for index, row in household_cols.iterrows():
    col_dict[row[0]] = row[1]

# create dict for column  names and description (final)
col_dict_clean = {}
for index, row in household_cols_clean.iterrows():
    col_dict_clean[row[0]] = row[1]

# get desired columns and insert YEAR and ID 
df_new = df[col_dict.keys()]
df_new.insert(loc = 0, column = 'YEAR', value = '2019')
df_new.insert(loc = 0, column = 'ID', value = df_new['YEAR'] + '_' + df_new['DUPERSID'].astype(str))

# list of survey waves to collapse 
combine = [['ACTDTY31','ACTDTY42','ACTDTY53'],['RTHLTH31','RTHLTH42','RTHLTH53'],['MNHLTH31','MNHLTH42','MNHLTH53'],['OFREMP31','OFREMP42','OFREMP53'],['EMPST31H','EMPST42H','EMPST53H']]

# collapse waves and drop them after collapsing
for sublist in combine:
    col_name = re.findall("[A-Za-z]+", sublist[0])[0]
    df_new = df_new.assign(**{col_name:pd.to_numeric(df[test_cols].bfill(axis=1).iloc[:, 0], errors='coerce')})
    df_new = df_new.drop(sublist, axis = 1)

# replace negatives with NaN
for col in df_new.columns:
    if df_new[col].dtype in ['int64','float64']:
        df_new.loc[df_new[col] < 0, col] = np.nan

# rename
# do this for remaining years
# combine with Prescribed Med Data