import pandas as pd
import numpy as np

# import data
df = pd.read_csv('h213a.csv')
# NOTE TO TEAM: TOOK OUT DOSAGE STRENGTH COLS AS HARD TO COMPARE
pmf_cols = pd.read_csv('pmf_columns.csv')
# only delta below is renaming description from year of first dose to years since first began taking medicine
pmf_cols_clean = pd.read_csv('pmf_columns_clean.csv') 

# Note: ndc opiod label from NYS for taxation purposes - going to see if this works
# Only has first 9 digits as it excludes final 2 for dosage size, so will match on 1st 9
# https://health.ny.gov/professionals/narcotic/docs/opioid_drug_listing.pdf
opioid_ndc = pd.read_csv('ndc_mme.csv', dtype={0: 'str'})
opioid_codes = set(opioid_ndc['9-Digit NDC'])

# create dict for column  names and description
col_dict = {}
for index, row in pmf_cols.iterrows():
    col_dict[row[0]] = row[1]

col_dict_clean = {}
for index, row in pmf_cols_clean.iterrows():
    col_dict[row[0]] = row[1]

# get desired columns and insert YEAR and ID 
df_new = df[col_dict.keys()]
year_value = '2019'
df_new.insert(loc = 0, column = 'YEAR', value = year_value)
df_new.insert(loc = 0, column = 'ID', value = df_new['YEAR'] + '_' + df_new['DUPERSID'].astype(str))

# replace negatives with NaN
for col in df_new.columns:
    if df_new[col].dtype in ['int64','float64']:
        df_new.loc[df_new[col] < 0, col] = np.nan
    else: # string / object types
        df_new.loc[df_new[col] == "-15", col] = np.nan

# Change year prescribed to years since taken dose - note some are 2020 for 2019 so do a max and count as 0 for current year

year_value = int(year_value)
df_new['RXBEGYRX'] = df_new['RXBEGYRX'].apply(lambda x: max(year_value-x, 0) if x > 0 else x)

##### THIS DIDN'T WORK - MAYBE NEED DIFF SOURCE?
df_new = df_new.assign(OPIOID_PRESCRIBED = lambda x: 1 if str(x)[0:9] in opioid_codes else 0)

# rename cols at end?
# do this for remaining years
# combine with other data