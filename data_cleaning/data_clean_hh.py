import pandas as pd
import numpy as np
import regex as re

# create list of data files
data_to_read = ['HC/HC_14.csv', 'HC/HC_15.csv', 'HC/HC_16.csv', 'HC/HC_17.csv', 'HC/HC_18.csv', 'HC/HC_19.csv']
years_to_read = ['2014', '2015', '2016', '2017', '2018', '2019']

# list of survey waves to collapse 
combine = [['ACTDTY31','ACTDTY42','ACTDTY53'],['RTHLTH31','RTHLTH42','RTHLTH53'],['MNHLTH31','MNHLTH42','MNHLTH53'],['OFREMP31','OFREMP42','OFREMP53'],['EMPST31H','EMPST42H','EMPST53H']]

def read_and_combine(data_to_read, years_to_read):
    # columns, both old and new
    household_cols = pd.read_csv('household_columns.csv')
    household_cols_clean = pd.read_csv('household_columns_clean.csv')

    # create dict for column names and description (both original and clean)
    col_dict = {}
    for index, row in household_cols.iterrows():
        col_dict[row[0]] = row[1]

    col_dict_clean = {}
    for index, row in household_cols_clean.iterrows():
        col_dict_clean[row[0]] = row[1]

    # loop through files 
    df_final = pd.DataFrame()
    for i, file in enumerate(data_to_read):

        df = pd.read_csv(file)
        # get desired columns
        year_value = years_to_read[i]
        print(data_to_read, year_value)
        for key in col_dict:
            if key not in df.columns:
                print(year_value, key)


        df_new = df[col_dict.keys()]
        df_new.insert(loc = 0, column = 'YEAR', value = year_value)
        df_new.insert(loc = 0, column = 'ID', value = df_new['YEAR'] + '_' + df_new['DUPERSID'].astype(str))
    
        # collapse waves and drop them after collapsing
        for sublist in combine:
            col_name = re.findall("[A-Za-z]+", sublist[0])[0]
            #df_new = df_new.assign(**{col_name:pd.to_numeric(df[sublist].bfill(axis=1).iloc[:, 0], errors='coerce')})
            df_new[col_name] = df[sublist].T.agg(','.join)
            df_new = df_new.drop(sublist, axis = 1)

        # replace negatives with NaN
        for col in df_new.columns:
            if df_new[col].dtype in ['int64','float64']:
                df_new.loc[df_new[col] < 0, col] = np.nan
        df_final = pd.concat([df_final, df_new])
    
    return df_final


def output_to_csv(df):
    '''
    Creates a csv of data
    
    Input:
        df (pd.df): df to convert
    
    Returns: csv
    '''
    df.to_csv('HC 2014-2019.csv')

output_to_csv(read_and_combine(data_to_read, years_to_read))
