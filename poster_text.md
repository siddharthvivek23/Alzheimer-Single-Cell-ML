# Multi-Scale Computational Analysis of Alzheimer’s Disease Using Single-Nucleus RNA-seq and Machine Learning

## Background

Alzheimer’s disease involves complex molecular and cellular changes across the brain. Single-nucleus RNA-seq can resolve cell-type-specific patterns, but the large number of cells in these datasets can obscure the much smaller number of independent biological samples.

## Research Question

**How do cell-type composition and transcriptomic patterns vary across amyloid/tau pathology states in Alzheimer’s disease, and do these patterns generalize across biological samples?**

## Dataset

**GSE243292 — NCBI GEO**

- 122,606 cells
- 26,423 genes
- 15 biological samples
- A−T−: **n = 2**
- A+T−: **n = 5**
- A+T+: **n = 8**

## Workflow

### Single-Nucleus RNA-seq

Normalization → PCA/UMAP → Cell-type characterization → Sample-level composition → Pathology analysis

### Machine Learning

Cells aggregated by biological sample → Training-only standardization/PCA → Leave-one-sample-out validation → Logistic regression → Held-out prediction

## Results: Cell-Type Composition

Cell-type proportions varied substantially across biological samples.

### Pathology Associations

| Cell type | Spearman ρ | p |
|---|---:|---:|
| **Inhibitory neurons** | **−0.584** | **0.022** |
| Astrocytes | +0.499 | 0.058 |
| Endothelial cells | +0.481 | 0.069 |
| OPCs | +0.341 | 0.214 |
| Excitatory neurons | −0.266 | 0.339 |
| Microglia | +0.174 | 0.534 |
| Oligodendrocytes | −0.050 | 0.861 |

Inhibitory neurons showed the strongest exploratory association.

**Benjamini-Hochberg FDR = 0.155**

**10,000-permutation p = 0.027**

### Inhibitory-Neuron Comparison

Mean inhibitory-neuron proportion:

- A−T−: **10.64%**
- A+T−: **13.48%**
- A+T+: **6.89%**

A+T− vs A+T+:

**Mann–Whitney U = 33, p = 0.0326**

This finding is **exploratory**, not a validated biomarker.

## Results: Sample-Level Machine Learning

An initial cell-level analysis produced approximately **70% accuracy**, but cells from the same biological sample could appear in both training and test sets.

Using leave-one-sample-out validation:

### Three-Class Model

- Accuracy: **46.7%**
- Balanced accuracy: **36.7%**
- Macro F1: **34.4%**

### Binary A+ vs A− Model

- A+: **n = 13**
- A−: **n = 2**
- Accuracy: **86.7%**
- Majority baseline: **86.7%**
- Balanced accuracy: **50.0%**
- Macro F1: **46.4%**
- Both A− samples predicted as A+

The 86.7% accuracy therefore did **not** indicate meaningful predictive discrimination.

## Conclusion

Single-nucleus RNA-seq revealed substantial heterogeneity in cell-type composition across Alzheimer’s pathology states.

Inhibitory-neuron abundance showed the strongest **exploratory** association, including lower proportions in A+T+ than A+T− samples, but the broader association did not remain significant after multiple-testing correction.

Most importantly, apparent cell-level machine-learning performance did not generalize when biological samples were properly held out.

**Sample-aware validation is critical when evaluating machine-learning models from single-cell transcriptomic data.**

## Key Takeaway

**Large numbers of cells do not equal large numbers of independent biological samples.**

Proper sample-level validation can substantially change the interpretation of machine-learning performance.
