# This script utilizes the TCGA2STAT package for convenient access to the TCGA 
# portal for dataset initiation.
library(TCGA2STAT)
# Download datasets into a list called 'PRAD'
PRAD <- getTCGA(disease = "PRAD", 
                data.type = "RNASeq2",
                p = getOption("mc.cores", 2L), 
                clinical = F)

