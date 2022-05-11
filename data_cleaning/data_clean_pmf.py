import pandas as pd
import numpy as np

# Create list of datafiles
data_to_read = ['PMEDS_14.csv', 'PMEDS_15.csv', 'PMEDS_16.csv', 'PMEDS_17.csv', 'PMEDS_18.csv', 'PMEDS_19.csv']
years_to_read = ['2014', '2015', '2016', '2017', '2018', '2019']

def read_and_combine(data_to_read, years_to_read):
    '''
    Reads and combines data

    Inputs:
        data_to_read (list of csv files): list of csv files to read in
        years_to_read (list of years files correspond to): years
    
    Returns (pd.df): Combined dataframe
    '''
    # Import col data for filtering
    # NOTE TO TEAM: TOOK OUT DOSAGE STRENGTH COLS AS HARD TO COMPARE; ALSO REMOVED DRUG NAME (RXDRGNAM) as matching on NDC 
    pmf_cols = pd.read_csv('pmf_columns.csv')
    # only delta below is renaming description from year of first dose to years since first began taking medicine
    pmf_cols_clean = pd.read_csv('pmf_columns_clean.csv') 

    # create dict for column  names and description
    col_dict = {}
    for _, row in pmf_cols.iterrows():
        col_dict[row[0]] = row[1]

    col_dict_clean = {}
    for _, row in pmf_cols_clean.iterrows():
        col_dict[row[0]] = row[1]
    
    # Note: ndc opiod label from NYS for taxation purposes - going to see if this works
    # Only has first 9 digits as it excludes final 2 for dosage size, so will match on 1st 9
    # https://health.ny.gov/professionals/narcotic/docs/opioid_drug_listing.pdf
    opioid_ndc = pd.read_csv('NDC_opioids.csv', dtype={0: 'str'})
    # opioid_ndc.insert(1, column='first_ndc_string', value=opioid_ndc['NDC'].str.split('-').str[0])
    # opioid_ndc.insert(2, column='second_ndc_string', value=opioid_ndc['NDC'].str.split('-').str[1])
    opioid_ndc.insert(1, column='NDC_clean', value=opioid_ndc['NDC'].str.replace('-', ""))
    opiod_ndc_prescribed = opioid_ndc[opioid_ndc['Product Type'] == 'Human Prescription Drug']
    opioid_codes = set(opiod_ndc_prescribed['NDC_clean'])

    for i, file in enumerate(data_to_read):
        df = pd.read_csv(file)
        # get desired columns and insert YEAR and IDsssssss
        df_new = df[col_dict.keys()]
        year_value = years_to_read[i]
        df_new.insert(loc = 0, column = 'YEAR', value = year_value)
        df_new.insert(loc = 0, column = 'ID', value = df_new['YEAR'] + '_' + df_new['DUPERSID'].astype(str))

    # replace negatives with NaN
    # NOTE still in progress as Wes's files are making me redo because it reads in number + text sometimes
        df_new.loc[df_new['PREGCAT'].apply(lambda x: np.nan if x.isdigit else x)]
        df_new.loc[df_new['RXFORM'].apply(lambda x: np.nan if x.isdigit else x)]
        for col in ['RXDAYSUP', 'PHARTP1', 'RXBEGYRX']:
            df_new.loc[df_new[col].apply(lambda x: int(x) if int(x.split(" ")[0]) > 0 else np.nan)]

    # Change year prescribed to years since taken dose - note some are 2020 for 2019 so do a max and count as 0 for current year

    year_value = int(year_value)
    df_new['RXBEGYRX'] = df_new['RXBEGYRX'].apply(lambda x: max(year_value-int(x), 0) if x != np.nan and int(x) > 0 else x)

    ##### ONLY GETTING LIKE 30 OPIOD_PRES...
    df_new = df_new.assign(OPIOID_PRESCRIBED = df_new['RXNDC'].apply(lambda x: 1 if str(x)[0:9] in opioid_codes or str(x)[0:10] in opioid_codes else 0))

    # rename cols at end?
    # combine with other data