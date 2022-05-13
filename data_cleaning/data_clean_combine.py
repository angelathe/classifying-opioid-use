# Import statements
import numpy as np
import pandas as pd

# Read in 3 databases

hc = pd.read_csv('HC 2014-2019.csv')
mc = pd.read_csv('MC 2014-2019.csv')
pmf = pd.read_csv('PMEDS 2014-2019.csv')

intermediate = hc.merge(pmf, how='inner', on='ID')

assert len(intermediate) == len(pmf), "Added or removed rows in merge"

final = intermediate.merge(mc, how='left', on='ID')

assert len(final) == len(pmf), "Added or removed rows in merge"

final.to_csv('final_data.csv')
