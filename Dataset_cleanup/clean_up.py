# -*- coding: utf-8 -*-
"""
Created on Tue May 24 17:13:54 2016

@author: ccthomps
"""
import feather
import numpy as np

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
