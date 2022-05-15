"""
File running models.

Classifying ***
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
from identification import vif_detection, corr_matrix_map

### Load in Data ###
data = pd.read_csv("final_data.csv")

to_drop = ["Unnamed: 0","Unnamed: 0_y","Unnamed: 0_x","Unnamed: 0.1","ID","YEAR_x","DUPERSID_x","DUPERSID",
            "YEAR", "ADHDAGED","YRSINUS","FOODMN_YEAR","OFREMP","AGE_YEARX","DOBMM","DOBYY", "opioid_prescriptions"]

vars = ["REGION_YEAR","AGELAST","SEX","RACETHX","MARRY_YEARX","EDUCYR",
"BORNUSA","FOODST_YEAR","TTLP_YEARX","FAMINC_YEAR","POVCAT_YEAR","POVLEV_YEAR","WAGEP_YEARX","UNEIMP_YEAR",
"DIVDP_YEARX","SALEP_YEARX","PENSP_YEARX","PUBP_YEARX","ADHDADDX","TRIMA_YEARX","MCRMA_YEAR","MCDMA_YEAR","ACTDTY",
"RTHLTH","MNHLTH","EMPST","non_opioid_prescriptions","NUM_CONDITIONS","INJURY"]

### Correlation Matrix (it looks like shit) ###
#corr_matrix_map(data,vars)

for col in data.columns:
    print(col,data[col].isnull().values.any())

#ADHD convert 2 to 0
data = data.drop(to_drop, axis = 1)
data["ADHDADDX"].apply(lambda x: x if x == 1 else 0)
data['ADHDADDX'] = data['ADHDADDX'].fillna(0)
data["EMPST"].apply(lambda x: 0 if x == 34 else 1)
data = data.rename({"YEAR_y": "YEAR", "DUPERSID_y": "DUPERSID"}, axis=1)
#DROPPED to_drop list, recoded ADHDADDX and EMPST

print(data.isna().sum())
data = data.dropna()
print(data.count()) 

#print(data["AGE_YEARX"].describe())
#print(data["AGELAST"].describe())
#data = data.drop("AGE_YEARX", axis = 1)
### Run identification ###
y = pd.DataFrame(data, columns=['opioid_prescribed_at_all'])
exog = pd.DataFrame(data, columns=vars)
#exog_vars = vif_detection(data,y,exog)
#exog_vars
max_vif = float('inf')
while max_vif > 5:
    reg_string = y.columns[0] + ' ~ ' + '+'.join(exog.columns)
    _, X = dmatrices(reg_string, data=data, return_type='dataframe')
    vif = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
    max_vif = max(vif[1:])
    if max_vif > 5:
        max_col = vif.index(max_vif)
        exog = exog.drop(exog.columns[max_col-1], axis=1)

exog

### Model 1-Logistic Regression
X=pd.DataFrame(exog).to_numpy()
y=pd.DataFrame(y).to_numpy()
scaler = StandardScaler()
X = scaler.fit_transform(X)
X_scaled = scaler.transform(X)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)
#log_reg = LogisticRegression().fit(X, y)
#log_reg = make_pipeline(StandardScaler(), LogisticRegression())
log_reg= LogisticRegression(max_iter = 1000).fit(X_train, y_train)  # apply scaling on training data
print("model score on training: %.3f" % log_reg.score(X_train, y_train))
print("model score on testing: %.3f" % log_reg.score(X_test, y_test))




decision_tree = tree.DecisionTreeClassifier()
decision_tree = decision_tree.fit(X_train, y_train)
score = decision_tree.score(X_test, y_test)
print("tree accuracy on testing: %.3f" % score)

