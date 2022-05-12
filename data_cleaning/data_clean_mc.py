'''
Data Cleaning - Medical Conditions File

CAPP 30254 - Machine Learning

Primary Coder: Angela The
'''

# Import statements
import numpy as np
import pandas as pd

# Reading in the data
data_to_read = ['MC/MC_14.csv', 'MC/MC_15.csv', 'MC/MC_16.csv', 'MC/MC_17.csv', 'MC/MC_18.csv', 'MC/MC_19.csv']
years_to_read = ['2014', '2015', '2016', '2017', '2018', '2019']


def read_and_combine(data_to_read, years_to_read):
    '''
    Reads and combines data

    Inputs:
        data_to_read (list of csv files): list of csv files to read in
        years_to_read (list of years files correspond to): years
    
    Returns (pd.df): Combined dataframe
    '''
    
    mc_cols = ['DUPERSID', 'CONDN', 'INJURY']
    df_final = pd.DataFrame()

    for i, file in enumerate(data_to_read):
        # Read individual data file
        df_raw = pd.read_csv(file)
        df = df_raw[mc_cols]
        year_value = years_to_read[i]

        # Check: # Columns
        assert list(df.columns) == mc_cols, "Incorrect columns in dataset"
        
        nunq_dupersid = df['DUPERSID'].nunique()
        n_df = len(df)
        n_inj_1 = df['INJURY'].value_counts(dropna=False)[1]
        
        # -------------- Recoding injury
        df['INJURY'] = df['INJURY'].apply(lambda x: 1 if x == "1 YES" else 0)

        # Check: Recoding injury
        assert df['INJURY'].value_counts(dropna=False)[1] == n_inj_1, "Injury recoding was incorrect"

        # -------------- Aggregating dataset to DUPERSID level
        df_agg = df.groupby(by="DUPERSID", as_index=False).agg(
            # Create new vars
            NUM_CONDITIONS = ('CONDN', 'count'),
            INJURY = ('INJURY', 'max'))

        # Checks
        assert len(df_agg) == df_agg['DUPERSID'].nunique(), "Aggregation not at DUPERSID level"

        assert nunq_dupersid == df_agg['DUPERSID'].nunique(), "# unique DUPERSIDs did not stay the same"

        assert sum(df_agg["NUM_CONDITIONS"]) == n_df, "Sum # of conditions not equal to raw dataset length"

        ct_inj_1 = df.loc[df['INJURY'] == 1]['DUPERSID'].nunique()
        assert df_agg['INJURY'].value_counts()[1] == ct_inj_1, "Num of Injury == 1 does not match original dataset"

        # -------------- Add year and unique yearly id
        year_value = str(year_value)
        df_agg.insert(loc = 0, column = 'YEAR', value = year_value)
        df_agg.insert(loc = 0, column = 'ID', 
                      value = df_agg['YEAR'] + '_' + df_agg['DUPERSID'].astype(str))

        df_final = pd.concat([df_final, df_agg])

    return df_final


def output_to_csv(df):
    '''
    Creates a csv of data
    
    Input:
        df (pd.df): df to convert
    
    Returns: csv
    '''
    df.to_csv('MC 2014-2019.csv')


# Run python3 to create aggregated file
output_to_csv(read_and_combine(data_to_read, years_to_read))