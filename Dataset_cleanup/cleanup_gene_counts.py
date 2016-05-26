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
    read_count = dataset.sum(axis = 1) #get the total reads for each sample
    for r in range(0,dataset.shape[0]) :
        dataset.iloc[r] = 1000000 * dataset.iloc[r] / read_count.iloc[r] #transform each read abundance (rsem) by the sample reads / million
    if sum(round(dataset.sum(axis = 1)) == 1e6) == 550 :  #the sum of each row in the transformed df should be 1000000.  if every row is transformed correctly, print statement
        print("\nTransformation Successful!\n\nTranscript abundance estimates have been transformed to transcripts per million reads")

transformation(gene_counts)
gene_counts.astype(float)
