# Alzheimer-Single-Cell-ML Research Write-Up

## Abstract

Alzheimer’s disease involves complex changes across multiple cell types, but transcriptomic patterns identified at the individual-cell level may not generalize across biological samples. This study investigated how cell-type composition and transcriptomic patterns vary across amyloid/tau pathology states using publicly available single-nucleus RNA-seq data from the NCBI Gene Expression Omnibus dataset GSE243292. The dataset contained 122,606 cells from 15 biological samples classified as A−T−, A+T−, or A+T+.

Cell-type proportions were calculated separately for each biological sample and evaluated in relation to pathology state. Inhibitory-neuron abundance showed the strongest exploratory association with ordinal pathology (Spearman ρ = −0.584, p = 0.022), although this association did not remain statistically significant after correction for multiple comparisons (FDR = 0.155). In a direct comparison, A+T+ samples also showed lower inhibitory-neuron proportions than A+T− samples, but this finding was treated as exploratory because of the limited number of biological samples and multiple-testing considerations.

Machine-learning analysis was evaluated using leave-one-sample-out validation to prevent cells from the same biological sample from appearing in both training and test sets. The three-class model achieved 46.7% accuracy, 36.7% balanced accuracy, and a macro F1 score of 34.4%. For binary A+ versus A− classification, accuracy was 86.7%, equal to the majority-class baseline, while balanced accuracy was 50.0% and macro F1 was 46.4%; both A− samples were classified as A+.

Together, these findings demonstrate substantial heterogeneity in cellular composition across pathology states while showing that apparent predictive performance from cell-level analyses may not generalize when biological samples are properly held out. The study highlights the importance of sample-aware validation when applying machine learning to single-cell transcriptomic data.

# Results

## Cell-Type Composition Across Pathology States

The single-nucleus RNA-seq dataset contained 122,606 cells from 15 biological samples spanning three amyloid/tau pathology states: A−T−, A+T−, and A+T+. Cell-type composition was calculated independently for each biological sample across seven major cell types: excitatory neurons (Ex), inhibitory neurons (In), oligodendrocytes (Oli), oligodendrocyte precursor cells (Opc), astrocytes (Ast), endothelial cells (End), and microglia (Mic).

Cell-type proportions varied substantially between biological samples, demonstrating considerable cellular heterogeneity within and across pathology groups. This variation motivated sample-level analysis rather than treating individual cells as independent biological observations.

Spearman correlations were calculated between each cell type’s sample-level proportion and ordinal pathology state. Inhibitory neurons showed the strongest association among the seven cell types (ρ = −0.5844, p = 0.0221). Astrocytes (ρ = 0.4992, p = 0.0581) and endothelial cells (ρ = 0.4814, p = 0.0692) showed weaker positive associations, while the remaining cell types showed weaker relationships.

After correction for multiple comparisons across the seven cell types, the inhibitory-neuron association did not remain statistically significant (FDR = 0.155). Therefore, the inhibitory-neuron result was treated as an exploratory signal rather than a confirmed pathology-associated biomarker.

## Inhibitory-Neuron Composition

Because inhibitory neurons showed the strongest exploratory correlation, their sample-level proportions were examined across pathology groups. The mean inhibitory-neuron proportion was 10.64% in A−T− samples, 13.48% in A+T− samples, and 6.89% in A+T+ samples.

A direct comparison between A+T− and A+T+ samples using a Mann–Whitney U test showed lower inhibitory-neuron proportions in the A+T+ group (U = 33, p = 0.0326). However, this comparison was interpreted cautiously because it was performed after examining multiple cell types, and the analysis included only five A+T− and eight A+T+ biological samples. The result therefore does not establish a validated biomarker, neuronal loss mechanism, or causal relationship with pathology.

Importantly, the proportions did not follow a simple monotonic progression across all three pathology groups, with A+T− samples showing a higher average inhibitory-neuron proportion than A−T− samples. The result is therefore better characterized as a difference associated with the A+T+ state rather than a uniformly progressive change across pathology.

## Sample-Level Machine Learning

The initial exploratory machine-learning analysis used individual cells as independent observations and produced approximately 70% classification accuracy. However, this strategy allows cells originating from the same biological sample to be distributed across both training and test sets. Because cells from the same sample share biological and technical characteristics, this splitting strategy can allow information about a biological sample to leak between the two datasets.

To address this issue, machine-learning evaluation was redesigned using leave-one-sample-out validation. Each biological sample was treated as the independent observation, with expression aggregated across cells within the sample. For each iteration, standardization and principal component analysis were fitted using only the training samples before a logistic regression model was trained and applied to the held-out sample.

For three-class classification of A−T−, A+T−, and A+T+ pathology states, the model achieved 46.7% accuracy, 36.7% balanced accuracy, and a macro F1 score of 34.4%. These values indicate limited generalization across held-out biological samples.

A binary model comparing A+ and A− samples achieved 86.7% accuracy, but this was identical to the majority-class baseline because 13 of the 15 samples were A+. Balanced accuracy was only 50.0%, and macro F1 was 46.4%. Both A− samples were classified as A+, demonstrating that the model did not recover meaningful predictive signal for the minority A− group under sample-level validation.

These results show that the approximately 70% accuracy observed in the original cell-level analysis should not be interpreted as evidence of robust biological prediction. Once biological samples were properly held out, model performance was substantially more limited.

## Overall Findings

Together, the analyses revealed substantial heterogeneity in cell-type composition across Alzheimer’s pathology states and identified inhibitory-neuron abundance as the strongest exploratory cell-type association. At the same time, sample-level machine-learning validation showed that predictive performance did not generalize reliably across independent biological samples.

The combined findings emphasize that single-cell datasets contain many observations but relatively few independent biological samples. Treating cells as independent training and testing observations can therefore produce overly optimistic estimates of predictive performance. Sample-aware validation provides a more conservative and biologically meaningful assessment of generalization.

# Methods

## Dataset

Single-nucleus RNA-seq data were obtained from the NCBI Gene Expression Omnibus (GEO) dataset GSE243292. The processed dataset contained 122,606 cells and 26,423 genes across 15 biological samples. Samples were categorized according to amyloid and tau pathology as A−T−, A+T−, or A+T+.

## Single-Cell Analysis

The single-cell analysis was performed using Python and Scanpy. Expression data were normalized and log-transformed, followed by highly variable gene selection and dimensionality reduction using principal component analysis (PCA) and uniform manifold approximation and projection (UMAP). Cell-type annotations were used to characterize excitatory neurons, inhibitory neurons, oligodendrocytes, oligodendrocyte precursor cells, astrocytes, endothelial cells, and microglia.

Cell-type composition was calculated independently for each biological sample as the percentage of cells assigned to each cell type. Spearman rank correlations were used to evaluate associations between sample-level cell-type proportions and ordinal pathology state. P values were corrected for multiple comparisons using the Benjamini-Hochberg procedure.

Because inhibitory neurons showed the strongest exploratory association, A+T− and A+T+ inhibitory-neuron proportions were additionally compared using a Mann–Whitney U test.

## Sample-Level Machine Learning

Machine-learning analysis was performed using logistic regression. Because individual cells from the same biological sample are not independent observations, the final analysis used biological-sample-level validation.

Cells were aggregated within each biological sample to produce one expression profile per sample. For each leave-one-sample-out (LOSO) iteration, the held-out biological sample was excluded from preprocessing and model fitting. Standardization and PCA were fitted using only the training samples, after which logistic regression was trained on the training samples and evaluated on the held-out sample.

Performance was evaluated using accuracy, balanced accuracy, macro F1 score, and confusion matrices. For binary A+ versus A− classification, the majority-class baseline was also reported because the dataset contained 13 A+ samples and only 2 A− samples.

# Discussion

## Interpretation of Findings

This analysis identified substantial variation in cell-type composition across the 15 biological samples. Inhibitory-neuron abundance showed the strongest exploratory association with ordinal pathology, but the association did not remain statistically significant after correction for multiple comparisons. The finding therefore provides a hypothesis for further investigation rather than evidence of a validated biomarker.

The lower inhibitory-neuron proportion observed in A+T+ compared with A+T− samples was also interpreted cautiously. The number of biological samples was small, and the comparison was conducted within a broader analysis of multiple cell types. In addition, inhibitory-neuron proportions did not decrease monotonically across all three pathology states, indicating that the observed pattern should not be interpreted as a simple progression of neuronal loss.

## Importance of Sample-Level Validation

The machine-learning analysis provided an important methodological finding. The initial cell-level analysis produced approximately 70% accuracy, but randomly dividing cells between training and testing can allow cells from the same biological sample to occur in both groups. This can lead to overly optimistic estimates because cells from the same sample share biological and technical characteristics.

When the analysis was redesigned using leave-one-sample-out validation, predictive performance was substantially more limited. The binary model's 86.7% accuracy was identical to the majority-class baseline, while balanced accuracy was 50.0%. Both A− samples were classified as A+, showing that the model did not demonstrate meaningful discrimination of the minority A− group.

These results demonstrate that high cell-level accuracy should not automatically be interpreted as evidence of generalizable biological prediction. In single-cell transcriptomic studies, the number of cells can be very large while the number of independent biological samples remains small. Validation strategies must therefore reflect the biological sampling structure of the experiment.

## Limitations

Several limitations should be considered when interpreting these findings. The analysis included only 15 biological samples, with particularly limited representation of the A− group. The small number of independent samples restricts statistical power and makes machine-learning evaluation challenging.

The inhibitory-neuron association did not survive multiple-testing correction and therefore should not be considered a statistically confirmed association. Similarly, the direct A+T− versus A+T+ comparison was exploratory.

The machine-learning results should also be interpreted as an evaluation of generalization within this dataset rather than as evidence that transcriptomic models cannot classify Alzheimer's pathology more broadly. Larger datasets containing more independent biological samples would be required to determine whether stronger predictive patterns generalize to new cohorts.

## Conclusion

The project demonstrates how single-nucleus RNA-seq can reveal substantial cellular heterogeneity across Alzheimer's pathology states while also illustrating the importance of biologically appropriate machine-learning validation.

The strongest exploratory biological signal involved inhibitory-neuron composition, but this finding requires validation in larger cohorts. More importantly, sample-level validation showed that apparent cell-level predictive performance did not translate into meaningful generalization across biological samples.

Together, these findings support a cautious, sample-aware approach to computational analysis of single-cell transcriptomic data in Alzheimer's disease.
