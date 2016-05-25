# -*- coding: utf-8 -*-
"""
Created on Tue May 24 17:13:54 2016

@author: ccthomps
"""
import feather
import numpy as np
import pandas as pd

#Import feather files that were downloaded and saved using TCGA2STAT package in R:
clinical = feather.read_dataframe('Clinical_data.feather')
gene_counts = feather.read_dataframe('Gene_counts.feather')

#Check data import:
if np.isfinite(clinical.shape[0]) :
    print("Clinical data set imported")
else :
    print("Error in Clinical data set import")

if np.isfinite(gene_counts.shape[0]) :
    print("Gene Counts data set imported")
else :
    print("Error in Gene_counts import")

"""The Clinical Data set will be cleaned such that only information available
at the onset of diagnosis is available.  This decision was made in order to
mimic the state of knowledge at the beginning of the patient's diagnosis."""
print(clinical.columns)
clinical.set_index(['clinical_index'], inplace=True) #set index to the TCGA ID
#clinical.drop(['clinical_index'], axis = 1, inplace = True) #drop the column now that it is the index
y = clinical['pathologyNstage'] #pull out the label (metastasis or no metastasis) as y
clinical.drop(['pathologyNstage'], axis = 1, inplace=True) #drop label from feature set
print(clinical.describe())

def useless_vars(dataset) :
    df = pd.DataFrame(dataset.describe())
    to_drop = df.columns[df.loc['unique'] <= 1]
    print("The following features do not provide any information:", to_drop.values, "and were dropped from the dataset")
    df.drop(to_drop, axis = 1, inplace = True)
    return(df)

clinical = useless_vars(clinical)
#print(clinical.head())
#clinical.drop(['Composite.Element.REF',
#        'gender', 'histologicaltype',
#       'numberoflymphnodes', 'pathologicstage', 'pathologyMstage',
#       'pathologyNstage', 'pathologyTstage', 'psavalue', 'race',
#       'radiationtherapy', 'residualtumor', 'tumortissuesite', 'vitalstatus',
#       'yearstobirth'], axis = 1, inplace = True)
