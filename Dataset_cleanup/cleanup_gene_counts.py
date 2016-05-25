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
names as columns.  Each value represents the abundance estimate for the gene in
each particular RNA-seq run.  This value is 'raw' in that it is not normalized
by the total number of reads made for the sample.  Thus the first step in data
clean-up is to transform these values to be normalized by the total number of
reads for the sample (in Millions)."""

gene_counts.set_index(['gc_index'], inplace = True) # set the index as the TCGA ID codes
print("")
#print(gene_counts.index[1:5]) [Debug]
print("Dimension of DataFrame:", gene_counts.shape)

def transformation(dataset) :
    read_count = dataset.sum(axis = 1)
    print(len(read_count), read_count[0:5])
    dataset.apply(lambda i : i / read_count, axis = 1)
    #dataset.apply(lambda rsem : 1000000 * rsem / rowsums, axis = 1)
    print(dataset.sum(axis=1))

transformation(gene_counts)
