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
    pmf_cols = pd.read_csv('pmf_columns.csv')

    # old columns we had but removed:
    # {RXDAYSUP: number of days prescribed, DRUGIDX: drug id (dupersid + counter), LINKIDX: ID FOR LINKAGE TO COND/OTH EVENT FILES
    # PHARTP1: TYPE OF PHARMACY PROV - 1ST, RXBEGYRX: Year PERSON STARTED TAKING MEDICINE, RXFORM: DOSAGE FORM (IMPUTED), PREGCAT: MULTUM PREGNANCY CATEGORY, 
    # RXNDC: NDC (national drug code), RXQUANTY: QUANTITY OF RX/PRESCR MED (IMPUTED)}

    # create dict for column  names and description
    col_dict = {}
    for _, row in pmf_cols.iterrows():
        col_dict[row[0]] = row[1]
    
    # CDC opioid agonist lists - NO LONGER IN USE AS MATCH ON TRIGGER WORDS (DIDN'T GET MANY MATCHES)
    # https://ndclist.com/pharma-class/
    # search for opioids, combine 3 lists
    # opioid_ndc = pd.read_csv('NDC_opioids.csv', dtype={0: 'str'})
    # opioid_ndc.insert(1, column='NDC_clean', value=opioid_ndc['NDC'].str.replace('-', ""))
    # opiod_ndc_prescribed = opioid_ndc[opioid_ndc['Product Type'] == 'Human Prescription Drug']
    # opioid_codes = set(opiod_ndc_prescribed['NDC_clean'])

    trigger_words = set(['acetaminophen', 'codeine', 'fentanyl', 'oxycodone', 'morphine', 'hydrocodone', 'oxycontin', 'tapentadol'])

    df_final = pd.DataFrame()

    for i, file in enumerate(data_to_read):
        df = pd.read_csv(file)
        # get desired columns
        df_new = df[col_dict.keys()]
        year_value = years_to_read[i]
        # replace negatives with NaN - no longer in use
        # NOTE still in progress as Wes's files are making me redo because it reads in number + text sometimes
        # df_intermediate = df_new.copy()
        # for col in ['PREGCAT', 'RXFORM']:
        #     df_intermediate[col] = df_new.loc[:, (col)].apply(lambda x: np.nan if x == "-15" or x == "-9" else x)
        # df_intermediate['RXNDC'] = df_new.loc[:, ('RXNDC')].apply(lambda x: np.nan if x == -15 else x)
        # for col in ['RXDAYSUP', 'PHARTP1', 'RXBEGYRX']:
        #     df_intermediate[col] = df_new.loc[:, (col)].apply(lambda x: int(x.split(" ")[0]) if int(x.split(" ")[0]) > 0 else np.nan)

        # Change year prescribed to years since taken dose - note some are 2020 for 2019 so do a max and count as 0 for current year
        # No longer in use
        # df_intermediate2 = df_intermediate.copy()
        # year_value = int(year_value)
        # df_intermediate2['RXBEGYRX'] = df_intermediate['RXBEGYRX'].apply(lambda x: max(year_value-int(x), 0) if x > 0 else x)

        ##### ONLY GETTING LIKE 30 OPIOD_PRES...
        #df_intermediate2 = df_intermediate2.assign(OPIOID_PRESCRIBED = df_new['RXNDC'].apply(lambda x: 1 if str(x)[0:9] in opioid_codes or str(x)[0:10] in opioid_codes else 0))
        
        # Revised assignment of opioids
        df_new = df_new.assign(OPIOID_PRESCRIBED = df_new['RXDRGNAM'].str.lower().str.contains('|'.join(trigger_words)))
        
        # Do 1 / 0 instead of T/F
        df_new['OPIOID_PRESCRIBED'] = df_new.OPIOID_PRESCRIBED.replace({True: 1, False: 0})

        # Get count of opioid and non-opioid prescriptions by id
        df_agg = df_new.groupby(by='DUPERSID', as_index=False).agg(
            opioid_prescriptions = ("OPIOID_PRESCRIBED", "sum"),
            total_prescriptions = ("OPIOID_PRESCRIBED", "count"),
            opioid_prescribed_at_all = ("OPIOID_PRESCRIBED", "max"))
        df_agg.insert(loc=3, column = 'non_opioid_prescriptions', value=df_agg['total_prescriptions'] - df_agg['opioid_prescriptions'])
        df_agg.drop(['total_prescriptions'], axis=1, inplace=True)

        # add year and unique yearly id
        year_value = str(year_value)
        df_agg.insert(loc = 0, column = 'YEAR', value = year_value)
        df_agg.insert(loc = 0, column = 'ID', value = df_agg['YEAR'] + '_' + df_agg['DUPERSID'].astype(str))

        print(year_value, 'dataframe original length: ', len(df),
              '\n', 'non-opioid presc', df_agg.non_opioid_prescriptions.sum(),
              '\n', 'opioid_presc', df_agg.opioid_prescriptions.sum(),
              '\n', 'total_prescriptions', df_agg.non_opioid_prescriptions.sum() + df_agg.opioid_prescriptions.sum(),
              '\n', 'unique_users_with_opioid_presc', df_agg.opioid_prescribed_at_all.sum(),
              '\n', 'total prescriptions = original df length:', df_agg.non_opioid_prescriptions.sum() + df_agg.opioid_prescriptions.sum() == len(df),
               '\n', 'percent_users_prescribed_opioids', df_agg.opioid_prescribed_at_all.sum() / len(df_agg) * 100)

        # concatenate years
        df_final = pd.concat([df_final, df_agg])

    print('total_opioid_prescriptions', df_final.opioid_prescriptions.sum(),
          '\n', 'non-opioid presc', df_final.non_opioid_prescriptions.sum(),
          '\n', 'unique_users_with_opioid_presc', df_agg.opioid_prescribed_at_all.sum(),
          '\n', 'percent_of_prescriptions_that_were_opioids',  df_final.opioid_prescriptions.sum() / (df_final.non_opioid_prescriptions.sum() + df_final.opioid_prescriptions.sum()) * 100,
          '\n', 'percent_users_prescribed_opioids', df_final.opioid_prescribed_at_all.sum() / len(df_final) * 100)
    return df_final

def output_to_csv(df):
    '''
    Creates a csv of data
    
    Input:
        df (pd.df): df to convert
    
    Returns: csv
    '''
    df.to_csv('PMEDS 2014-2019.csv')

output_to_csv(read_and_combine(data_to_read, years_to_read))
