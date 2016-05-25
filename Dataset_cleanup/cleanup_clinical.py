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
clinical.set_index(['clinical_index'], inplace=True) #set index to the TCGA ID

y = clinical['pathologyNstage'] #pull out the label (metastasis or no metastasis) as y
clinical.drop(['pathologyNstage'], axis = 1, inplace=True) #drop label from feature set

def useless_vars(dataset) :
    df = pd.DataFrame(dataset.describe())
    to_drop = df.columns[df.loc['unique'] <= 1]
    print("\n\n","The following features do not provide any information:","\n",to_drop.values,"\n")
    dataset.drop(to_drop, axis = 1, inplace = True)
    return(dataset)

def future_vars(dataset) :
    df = pd.DataFrame({'Known_at_diagnosis' : '?'}, index = dataset.columns)
    df.loc['dateofinitialpathologicdiagnosis']['Known_at_diagnosis'] = 'yes'
    df.loc['daystolastfollowup']['Known_at_diagnosis'] = 'no'
    df.loc['daystodeath']['Known_at_diagnosis'] = 'no'
    df.loc['daystopsa']['Known_at_diagnosis'] = 'no'
    df.loc['gleasonscore']['Known_at_diagnosis'] = 'maybe'
    df.loc['histologicaltype']['Known_at_diagnosis'] = 'no'
    df.loc['numberoflymphnodes']['Known_at_diagnosis'] = 'no'
    df.loc['pathologyTstage']['Known_at_diagnosis'] = 'no'
    df.loc['psavalue']['Known_at_diagnosis'] = 'yes'
    df.loc['race']['Known_at_diagnosis'] = 'yes'
    df.loc['residualtumor']['Known_at_diagnosis'] = 'no'
    df.loc['radiationtherapy']['Known_at_diagnosis'] = 'no'
    df.loc['vitalstatus']['Known_at_diagnosis'] = 'no'
    df.loc['yearstobirth']['Known_at_diagnosis'] = 'yes'
    keep = df[df['Known_at_diagnosis'] != 'no'].index
    dropped = df[df['Known_at_diagnosis'] == 'no'].index
    dataset.drop(dropped.values, axis = 1, inplace = True)
    print("\n\n","Variables that are not known at initial diagnosis:","\n", dropped.values, "\n")
    return(dataset)

clinical = useless_vars(clinical)
clinical = future_vars(clinical)
print(clinical.head())
print("Dimensions of clinical dataframe:", clinical.shape)
