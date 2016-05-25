import feather
import numpy as np
import pandas as pd

#Import feather files that were downloaded and saved using TCGA2STAT package in R:
gene_counts = feather.read_dataframe('Gene_counts.feather')

#Check data import:
if np.isfinite(gene_counts.shape[0]) :
    print("Gene Counts data set imported")
else :
    print("Error in Gene_counts import")

 """Gene Counts dataframe are formatted with patient ID as the index and gene
 names as columns.  Each value represents the RSEM value for the specific RNA-seq
 run.  This value is 'raw' in that it is not normalized by the total number of reads
 for the sample.  Thus the first step in data clean-up is to transform these
 values to be normalized by the total number of reads for the sample (in
 Millions)."""
