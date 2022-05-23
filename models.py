"""
File running models.

Classifying Opioid Prescription
May 2022
"""
###Load in relevant packages
#from tkinter import Y
import numpy as np
import pandas as pd
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from statsmodels.stats.outliers_influence import variance_inflation_factor
from sklearn import preprocessing
from patsy import dmatrices
from sklearn.linear_model import LogisticRegression
from sklearn import tree
from identification import vif_detection

### Load in Data ###
data = pd.read_csv("data_cleaning/final_data.csv")


vars = ["REGION_YEAR","AGELAST","SEX","RACETHX","MARRY_YEARX","EDUCYR",
"BORNUSA","FOODST_YEAR","TTLP_YEARX","FAMINC_YEAR","POVCAT_YEAR","POVLEV_YEAR","WAGEP_YEARX",
"DIVDP_YEARX","SALEP_YEARX","PENSP_YEARX","PUBP_YEARX","ADHDADDX","ACTDTY",
'UNINSURED_ONLY', 'PRIVATE_ONLY', 'MEDICAID_ONLY', 'MEDICARE_ANY', 'MEDICARE_ADV', 'MEDICARE_MEDICAID', 'MEDICARE_PRIVATE',	
"RTHLTH","MNHLTH","EMPST","non_opioid_prescriptions","NUM_CONDITIONS","INJURY"]

data = data.dropna()

### Run identification ###
y = pd.DataFrame(data, columns=['opioid_prescribed_at_all'])
exog = pd.DataFrame(data, columns=vars)
exog_vars = vif_detection(data,exog, y)

### Model 1-Logistic Regression
X=pd.DataFrame(exog).to_numpy()
y=pd.DataFrame(y).to_numpy().reshape(len(y),)
scaler = StandardScaler()
X = scaler.fit_transform(X)
X_scaled = scaler.transform(X)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)
log_reg= LogisticRegression(max_iter = 1000).fit(X_train, y_train)  # apply scaling on training data
print("model score on training: %.3f" % log_reg.score(X_train, y_train))
print("model score on testing: %.3f" % log_reg.score(X_test, y_test))

decision_tree = tree.DecisionTreeClassifier()
decision_tree = decision_tree.fit(X_train, y_train)
score = decision_tree.score(X_test, y_test)
print("tree accuracy on testing: %.3f" % score)

