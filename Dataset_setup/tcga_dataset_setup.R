# This script utilizes the TCGA2STAT package for convenient access to the TCGA 
# portal for dataset initiation.

#package import
library(TCGA2STAT)
library(feather)

# Download datasets into a list called 'PRAD'
PRAD <- getTCGA(disease = "PRAD", 
                data.type = "RNASeq2",
                p = getOption("mc.cores", 2L), 
                clinical = T)

#wrangle into data_frame
data.frame(t(PRAD[[1]]), stringsAsFactors = FALSE) -> gc #Gene counts 
gc <- cbind("gc_index" = row.names(gc), gc)
data.frame(PRAD[[2]], stringsAsFactors = FALSE) -> clinical
clinical <- cbind("clinical_index" = row.names(clinical), clinical) #move row names to first column
gc$gc_index <- sapply(gc$gc_index, substr, 0, 12) #shorten extended ID to the standard 12 characters observed in clininical data set

#write files to be picked up in python
write_feather(gc, "Gene_counts.feather") 
write_feather(clinical, "Clinical_data.feather")
