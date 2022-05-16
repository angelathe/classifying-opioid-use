# Classifying Opioid Prescription Using Machine Learning Techniques
CAPP 30254—Machine Learning for Public Policy \
Group Members: Wesley Janson, Matt Kaufmann, Piper Kurtz, Angela The, Eujene Yum


## Data Cleaning
- Note: All files are located in the folder **data_cleaning**

- **data_clean_hh.py**: Python script to perform data cleaning on the Household Component (HC) datasets from 2014-2019.

- **data_clean_pmf.py**: Python script to perform data cleaning and aggregation on the Prescribed Medicine (PMF) datasets from 2014-2019.

- **data_clean_mc.py**: Python script to perform data cleaning and aggregation on the Medical Conditions (MC) datasets from 2014-2019.

- **data_clean_mc.ipynb**: Notebook file to explore the Medical Conditions (MC) datasets and perform initial summary statistics on the aggregated dataset.

- **data_clean_combine.py**: Python script to merge the following cleaned (and aggregated) datasets together (on ID, 2014-2019): 1) Household Component, 2) Prescribed Medicine, and 3) Medical Conditions.


## Main directory
- **identification.py**: Python script with functions assisting in identification of relevant feature variables to include in 
    models. These functions are VIF Identification and Correlation matrix heatmap creation (useless and uninterpretable) 
    both called in models.py.

- **models.py**: Main Python script used to create Logistic regression, decision tree, and neural network models for analysis.