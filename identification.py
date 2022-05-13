"""
Identifying relevant variables to be used in ML models.

Classifying ***
May 2022
"""
### Load in relevant packages
from statsmodels.stats.outliers_influence import variance_inflation_factor
from patsy import dmatrices
import numpy as np
import pandas as pd
import seaborn as sn
import matplotlib.pyplot as plt

##### HELPER FUNCTIONS #####
# Variance Inflation Factor #
def vif_detection(dataset,exog_vars,dep_var):
    '''
    Method computing Variance Inflation Factors (VIF) on prospective exogenous variables for regression. 
    5 (inclusive) is used as the cutoff for multicollinearity. This function eliminiates the variable with 
    the highest VIF, and reruns the regression until the highest VIF is below the threshold.

    Input:
        -dataset (pandas df): pandas dataframe with complete dataset
        -exog_vars (pandas df): pandas dataframe of potential exogenous variables for regression.
        -dep_var (pandas series): pandas dataframe of dependent variable in regression.
    '''
    max_vif = float('inf')
    while max_vif > 5:
        reg_string = dep_var.columns[0] + ' ~ ' + '+'.join(exog_vars.columns)
        _, X = dmatrices(reg_string, data=dataset, return_type='dataframe')
        vif = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
        max_vif = max(vif[1:])
        if max_vif > 5:
            max_col = vif.index(max_vif)
            exog_vars = exog_vars.drop(exog_vars.columns[max_col-1], axis=1)

    return exog_vars


### Correlation Matrix???-Might be too much Yeah
def corr_matrix_map(dataset,variables):
    '''
    Helper function designed to take input variables and compute correlation
    matrix with heatmap features for easy comparison.

    Input:
        -dataset (pandas df): pandas dataframe with complete dataset
        -variables (list): list of variable names from "dataset" that will
            appear in correlation matrix.
    '''
    df = pd.DataFrame(dataset,columns=variables)
    corrMatrix = df.corr()
    sn.heatmap(corrMatrix, annot=True)
    plt.show()


### Run PCA on data???





