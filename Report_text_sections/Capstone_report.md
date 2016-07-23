# Definition
## Project Overview
The prostate is a glandular organ of the male reproductive system that helps to
control urinary and reproductive functions.  According to the charity Prostate
Cancer UK, one in eight British men will  be diagnosed with prostate
adenocarcinoma (prostate cancer, henceforth 'PC') in their  lifetime {citation}.
Men over 50 years of age are often subjected to routine digital examinations, or
urine test (the 'PCA' test) for signs of PC.  However the gold standard
diagnosis is the Gleason test.  In brief, a series of small needle sized
biopsies are taken from the patient's prostate gland.  Each biopsy is processed
and scored by a pathologist for signs of abnormal cell type and
structure.  Gleason scores ranging from 2 to 5 are considered not
malignant, whereas scores ranging from 6-10 are considered malignant and provide
an added estimation of severity (Humphrey, 2004).

Contrary to some types of cancer, malignancies that remain local within the
prostate are rarely lethal (survival rate of ~99%) {citation}.  However, if a
malignancy born of the prostate undergoes metastasis (the process of cancer cell
migration to other sites in the body), the survival rate drops to ~28%.  Because
of this discrepancy, many men opt for radical prostatectomy (surgical removal of the
entire prostate).  While ensuring prevention of metastasis, removal of the
prostate results in high morbidity, e.g. inability to control urination, loss of
sexual function, etc.

Unfortunately, there are currently no prognostic tests for PC metastasis.  The
patient data  that is typically available at the time of diagnosis is not rich
enough to accurately predict the likelihood of prostate cancer metastasis
{citation}.   A model that is able to predict whether an untreated malignancy
would be likely to remain locally within the prostate or to metastasize could be
an invaluable tool on whether prostatectomy (and the associated morbidity) is
necessary.  To generate such a model, a more distinguishing set of feature data
is required.

One potential solution to this problem is an RNA-seq profile.  In brief, RNA-seq
is a technique that reads and counts RNA sequences in a sample.  When a gene is
activated in a cell, the DNA sequence is read ('transcribed') into an RNA
sequence.  Thus by reading all of the RNA molecules that exist in a sample, one
may determine which genes have been activated, and to what degree.  A gene count
profile is the estimation of activation for the full set of known human genes.

As metastatic cancer cells behave in drastically different ways than malignant
cells that remain local, there must be an inherent difference in gene activation
between the two cell types.   This difference may be detectable, however there
are likely to be many different genetic paths towards metastasis. Thus it is
unlikely that a single gene could distinguish metastasis state and local
malignancy. The ultimate goal of this project is to determine whether the
RNA-seq profile taken from a cancerous prostate biopsy during initial
presentation and diagnosis, is  sufficient for prognosis of prostate cancer
metastasis.

## Problem Statement
The primary questions that this project aims to answer are :

* Can prostate cancer metastasis state be predicted from a gene activation
(RNA-seq) profile?

* If so, what genes (individually or in concert) are important for this
classification?

The goal of this project is to design a model that predicts Prostate Cancer
metastasis using the gene activation profile derived from the patient's prostate
biopsy, taken at the initial Gleason Test diagnosis phase.

To acheive this goal, it is likely that a  significant feature reduction
exercise will be necessary, as each  RNA-seq profile quantifies expression of
20501 human genes.  After Feature Reduction, several classification algorithms
will be employed and tested for predictive performance.  A final model will be
built and optimized. Finally, a function or application will be engineered that
receives an RNA-seq profile as an input and outputs a prediction for future
metastasis.

## Metrics
As this problem has been defined, a performance metric for classification is
required.  The standard classification metric is the accuracy score, i.e. the
percentage of observations which were correctly classified.  However several
aspects of this project which make accuracy unsuitable.  First, metastasis is a
somewhat rare event, which has lead to an unbalanced label prevalence within the
data set. The use of accuracy to score a model for unbalanced data can be
misleading.  For example, in a data set where 90% belong to the negative class,
a model that predicts every observation as 'negative' will achieve a seemingly
respectable 0.9 accuracy score.  Yet this strategy clearly contravenes the point
of generating a model for prediction in the first place.  Secondly, the
consequences of calling a False-negative (FN) or a False-positive (FP) are not
equal in this project.  For instance, a metastasis that is missed (FN) could
lead to mortality, whereas a local malignancy that is called as a metastasis
(FP), would lead to an unnecessary morbidity, but would not be lethal.  Accuracy
does not distinguish FP or FN in its calculation.

To address the issue of unbalanced data, one could use a metric such as the
Matthew's Correlation Coefficient (MCC).

$$MCC = \frac{TP x TN - FP x FN}{\sqrt{(TP+FP)(TP+FM)(TN+FP)(TN+FN)}}$$

This metric ranges from -1 to 1, with zero being the score expected from a model
that guesses randomly.  It provides an intuitive performance metric without a
reviewers prior knowledge of class balance.  However, the MCC does not
distinguish among the different consequences of FP and FN prediction in model
performance.

For this purpose, the $F\beta$ score could be used.  While the F1 score is the
harmonic mean between the precision and recall of the named positive label, a
beta parameter may be introduced in order to alter the importance of recall
versus precision within the model performance metric.  Setting \beta to 2
weights recall as twice as important than precision, and is called the F2 score.

$$F1 = \frac{2TP}{2TP+FN+FP}$$

$$F_\beta = (1+ \beta^2) \frac{precision\, x\, recall}{(\beta^2\, x\,
precision)\,+\,recall}$$

For the purposes of this project, recall of metastasis is the most important
feature of model performance, however precision is not insignificant.  Therefore
an F2 score was implemented (i.e. $F_\beta$, with $\beta := 2$) as the main
performance metric.  To ensure no model was 'gaming' the performance measure, I
chose to include the MCC value in each assessment as a control for balanced
accuracy.

# Analysis
## Data Exploration
'The Cancer Genome Atlas'(TCGA) is a research consortium set up to curate
clinical data from thousands of patient participants, covering an array of
cancer types.   Provided data includes basic clinical information as well as DNA
and RNA sequencing of cancer biopsies. These data sets are updated frequently as
new information becomes available.  Thus each data download represents a
snapshot in an evolving data set.

While detailed genomic and RNA sequence data is control-accessed, pre-processed
gene count data is publicly available.  Data can be downloaded via the
consortium  portal or acquired into dataframe format using a package in the R
language.  If the script, 'Dataset_setup/tcga_dataset_setup.R' is run in R, then
two feather files (which can be read by many languages, including python) will
be stored in the working directory for the clinical, and gene count datasets,
respectively.  The versions stored in the submission repository are current at
the time of submission.

The clinical data set contains 22 features, of which several are irrelevant
(e.g. all prostate cancer patients are 'male').  Features with a single
categorical class were removed in the 'Dataset_cleanup/cleanup_clinical.py'
script.  Then, in order to mimic the knowledge state a doctor/patient would
encounter upon presentation, features were limited to only those that would be
known prior to Gleason score analysis.  This includes the age of the patient,
and the patient's PSA (prostate secreted antigen) test score.  The outcome
variable for this project is contained in the clinical data set, which is
'pathologyNstage'.  This label is composed of 'n0' or 'n1', representing local
versus metastatic cancer, respectively.  Unfortunately of the 499 patients
enrolled in the study, 73 records did not include the metastasis state.

The primary data set for this project is the gene count matrix.  This data set
provides a value for gene expression level for every known human gene.  The same
patient index links the clinical data set to the  gene count data set, of which
497 are common among the two.  As the expression values for each patient are not
normalized, an important step prior to analysis was to transform each value to
the transcript count per million reads (TPM).  This transformation normalizes
such that the expression levels for each patient are now comparable.  A test was
run after transformation to ensure that each patient profile totaled 1 million
reads.  The next section will serve to describe the clinical data and provide a
benchmark prognosis rate using information available to a doctor at
presentation.   

## Exploratory Visualization
Frequency of metastasis is a relatively rare occurrence for prostate
adenocarcinoma, a trend that is also reflected in the TCGA cohort data,
as shown in Figure 1.

![Figure 1](/Label_count.png)

**Figure 1** - Frequency of Metastasis in the TCGA Prostate adenocarcinoma
cohort.

When grouped by Gleason score, it is also evident that
metastasis rates increase as the severity of cancer increases (Figure 2).  This
is  intuitive, yet clearly not sufficient to determine whether a specific
cancer, regardless of Gleason score, will metastasize or not.  To illustrate,
cancers that have been rated at a Gleason score of '9' are still more likely to
belong to the 'n0' class than the metastasis class.

![Figure 2](/Gleason_hist.png)

**Figure 2** - Frequency of Metastasis state grouped by Gleason score.


## Algorithms and Techniques
The data set to be used in this project is both wide, and unbalanced - meaning
that in its original form, the data set contains many more features than
observations, and that the class labels for each observation exist in an
unbalanced ratio.  As such, the types of algorithms that can be implemented
successfully must reflect this.  Also important towards a successful outcome,
will be feature reduction exercise. Finding a signal, if any, within the noise
of a wide data set will be paramount to the success of this project.

There are a variety of techniques for feature reduction, including the filtering
features that exhibit some degree of utility in label separation individually,
or wrapping functions that recursively test combinations of features for
performance in a given base model.  
