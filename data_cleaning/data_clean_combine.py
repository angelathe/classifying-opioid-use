# 1. Import statements
import numpy as np
import pandas as pd


# 2. Read in 3 databases
hc = pd.read_csv('HC 2014-2019.csv')
mc = pd.read_csv('MC 2014-2019.csv')
pmf = pd.read_csv('PMEDS 2014-2019.csv')


# 3. Merge datasets
intermediate = hc.merge(pmf, how='inner', on='ID')

assert len(intermediate) == len(pmf), "Added or removed rows in merge"

final = intermediate.merge(mc, how='left', on='ID')

assert len(final) == len(pmf), "Added or removed rows in merge"


# 4. Final data cleaning
to_drop = ["Unnamed: 0","Unnamed: 0_y","Unnamed: 0_x",
           #"Unnamed: 0.1",
           "ID","YEAR_x","DUPERSID_x","DUPERSID","DUPERSID_y",
            "YEAR", "UNEIMP_YEAR", "ADHDAGED","YRSINUS","FOODMN_YEAR","OFREMP","AGE_YEARX","DOBMM","DOBYY", "opioid_prescriptions"]

# for col in data.columns:
#     print(col,data[col].isnull().values.any())

# ADHD convert 2 to 0
final_clean = final.drop(to_drop, axis = 1)
final_clean["ADHDADDX"].apply(lambda x: x if x == 1 else 0)
final_clean['ADHDADDX'] = final_clean['ADHDADDX'].fillna(0)
final_clean["EMPST"].apply(lambda x: 0 if x == 34 else 1)
final_clean = final_clean.rename({"YEAR_y": "YEAR"}, axis=1)


# 5. Export final CSV file
final_clean.to_csv('final_data.csv')
