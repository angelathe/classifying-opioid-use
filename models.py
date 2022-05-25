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
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.datasets import make_classification
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
X=pd.DataFrame(exog_vars).to_numpy()
y=pd.DataFrame(y).to_numpy().reshape(len(y),)
scaler = StandardScaler()
X = scaler.fit_transform(X)
X_scaled = scaler.transform(X)
X_train, X_test_valid, y_train, y_test_valid = train_test_split(X_scaled, y, random_state=42, test_size = 0.2)
X_valid, X_test, y_valid, y_test = train_test_split(X_test_valid, y_test_valid, random_state=42, test_size = 0.5)
log_reg= LogisticRegression(max_iter = 1000).fit(X_train, y_train)  # apply scaling on training data
print("model score on training: %.3f" % log_reg.score(X_train, y_train))
print("model score on testing: %.3f" % log_reg.score(X_test, y_test))

### Model 2-Decision Tree
decision_tree = tree.DecisionTreeClassifier()
decision_tree = decision_tree.fit(X_train, y_train)
score = decision_tree.score(X_test, y_test)
print("tree accuracy on testing: %.3f" % score)

### Model 3-Random Forest
forest_model = RandomForestClassifier(random_state = 0, n_jobs = 1, n_estimators = 100, class_weight = 'balanced')
forest_model = forest_model.fit(X_train, y_train)
score = forest_model.score(X_test, y_test)
print("random forest accuracy on testing: %.3f" % score)

### Model 4-Neural Net
clf = MLPClassifier(hidden_layer_sizes = (100,50, 25), activation = 'logistic', alpha = 0.0001, solver = 'sgd', max_iter = 200, shuffle = True, random_state=1).fit(X_train, y_train)
#clf = MLPClassifier(hidden_layer_sizes = (100,50, 25), random_state=1, max_iter=300).fit(X_train, y_train)
score = clf.score(X_test, y_test)
print("neural net accuracy on testing: %.3f" % score)

### Model 5-Ada Boost? 
# adjust number of estimators
ada_boost = AdaBoostClassifier(n_estimators=1000, learning_rate=0.2, algorithm='SAMME.R', random_state=1).fit(X_train, y_train)
score = ada_boost.score(X_test, y_test)
print("Ada  accuracy on testing: %.3f" % score)