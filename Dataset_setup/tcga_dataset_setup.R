# This script utilizes the TCGA2STAT package for convenient access to the TCGA 
# portal for dataset initiation.
library(TCGA2STAT)
# Download datasets into a list called 'PRAD'
PRAD <- getTCGA(disease = "PRAD", 
                data.type = "RNASeq2",
                p = getOption("mc.cores", 2L), 
                clinical = T)
data.frame(t(PRAD[[1]])) -> gc #Gene counts 
data.frame(PRAD[[2]]) -> clinical
#write files to be picked up in python
library(feather)
write_feather(gc, "Gene_counts.feather") 
write_feather(clinical, "Clinical_data.feather")
##Need to fix so that row names are not dumped during feather save.