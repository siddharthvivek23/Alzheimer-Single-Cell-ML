
# Alzheimer's Single-Cell and Machine Learning Analysis

Independent computational analysis of Alzheimer's disease using single-nucleus RNA-seq data and machine learning.

## Project Overview

This project investigates cell-type-specific molecular patterns associated with Alzheimer's disease using publicly available single-nucleus RNA-seq data.

The analysis combines exploratory single-cell analysis with machine learning to examine whether transcriptomic features can distinguish Alzheimer's pathology groups and identify predictive molecular signatures.

## Dataset

Single-nucleus RNA-seq data were obtained from the NCBI Gene Expression Omnibus (GEO):

**GSE243292**

## Single-Cell RNA-seq Analysis

The single-cell workflow includes:

* Quality control and filtering
* Normalization and log transformation
* Highly variable gene selection
* PCA and UMAP dimensionality reduction
* Cell-type-specific analysis
* APOE and TREM2 expression analysis
* Cellular composition analysis across pathology groups

### Tools

* Python
* Scanpy
* AnnData
* Pandas
* Matplotlib

## Machine Learning Analysis

A logistic regression model was used to investigate whether transcriptomic features could classify Alzheimer's pathology groups.

The workflow includes:

* Highly variable gene selection
* Feature extraction from single-cell RNA-seq data
* Logistic regression classification
* Train/test model evaluation
* Confusion matrix analysis
* Gene feature-importance analysis
* Identification of predictive genes

### Tools

* Python
* scikit-learn
* Pandas
* Scanpy
* AnnData
* Joblib

## Repository Structure

* `Single_Cell_RNAseq/` — Single-nucleus RNA-seq preprocessing, visualization, cell-type analysis, and pathology-associated analysis
* `Machine_Learning/` — Logistic regression classification, model evaluation, and predictive gene analysis

## Research Focus

The overall goal is to connect **single-cell transcriptomic patterns** with **machine learning-based prediction of Alzheimer's pathology**, with particular attention to cell-type-specific molecular signatures.

## Author

**Siddharth Vivek**
