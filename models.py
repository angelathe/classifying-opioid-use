"""
File running models.

Classifying ***
May 2022
"""
###Load in relevant packages
#from tkinter import Y
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from identification import vif_detection, corr_matrix_map

### Load in Data ###
data = pd.read_csv("final_data.csv")

### Correlation Matrix (it looks like shit) ###
to_drop = ["Unnamed: 0","Unnamed: 0_x","Unnamed: 0.1","ID","YEAR_x","DUPERSID_x","YEAR","DUPERSID", "ADHDAGED", "YRSINUS","FOODMN_YEAR", "OFREMP"]
# Let's check for missing values/NAs, something is awry
# Make "YEAR" a float
vars = ["REGION_YEAR","AGE_YEARX","AGELAST","DOBMM","DOBYY","SEX","RACETHX","MARRY_YEARX","EDUCYR",
"BORNUSA","YRSINUS","FOODST_YEAR","FOODMN_YEAR","TTLP_YEARX","FAMINC_YEAR","POVCAT_YEAR","POVLEV_YEAR","WAGEP_YEARX","UNEIMP_YEAR",
"DIVDP_YEARX","SALEP_YEARX","PENSP_YEARX","PUBP_YEARX","ADHDADDX","ADHDAGED","TRIMA_YEARX","MCRMA_YEAR","MCDMA_YEAR","ACTDTY",
"RTHLTH","MNHLTH","OFREMP","EMPST","opioid_prescriptions","non_opioid_prescriptions","YEAR","DUPERSID","NUM_CONDITIONS","INJURY"]

corr_matrix_map(data,vars)

for col in data.columns:
    print(col,data[col].isnull().values.any())

#ADHD convert 2 to 0
data = data.drop(to_drop, axis = 1)
data["ADHDADDX"].apply(lambda x: x if x == 1 else 0)
data['ADHDADDX'] = data['ADHDADDX'].fillna(0)
data["EMPST"].apply(lambda x: 0 if x == 34 else 1)
#DROPPED to_drop list, recoded ADHDADDX and EMPST

print(data.isna().sum())
data = data.dropna()
print(data.count()) 
print(data["AGE_YEARX"].describe())
print(data["AGELAST"].describe())
data = data.drop("AGE_YEARX", axis = 1)
### Run identification ###
y = pd.DataFrame(data, columns=['opioid_prescribed_at_all'])
exog = pd.DataFrame(data, columns=vars)
exog_vars = vif_detection(data,y,exog)
exog_vars

### Model 1-Logistic Regression
#X=pd.DataFrame(exog).to_numpy()
#y=pd.DataFrame(y).to_numpy()
#log_reg = LogisticRegression(random_state=0).fit(X, y)
# log_reg