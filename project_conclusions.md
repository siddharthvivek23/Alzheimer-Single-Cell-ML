# Project Conclusions

This project investigated how cell-type composition and transcriptomic patterns vary across Alzheimer's disease pathology states using single-nucleus RNA-seq data from GSE243292.

## Cell-Type Composition

Cell-type proportions varied substantially across biological samples and pathology states.

Among the seven analyzed cell types, inhibitory neurons showed the strongest exploratory association with ordinal pathology state:

* Spearman rho = **−0.584**
* Unadjusted p = **0.022**
* FDR = **0.155**

Because the association did not remain significant after multiple-testing correction, it should be considered an **exploratory finding rather than a validated association**.

A direct comparison also showed lower inhibitory-neuron proportions in A+T+ samples than in A+T− samples. However, the limited number of biological samples and the broader analysis of multiple cell types mean this result should also be interpreted cautiously.

## Sample-Level Machine Learning

An initial cell-level logistic regression analysis produced approximately 70% accuracy. However, randomly splitting individual cells can place cells from the same biological sample in both the training and testing sets, allowing biological-sample information to leak between the two groups.

To address this, the machine-learning analysis was redesigned using **leave-one-sample-out validation**, with biological samples treated as the independent units.

For three-class pathology classification, the sample-level model achieved:

* Accuracy: **46.7%**
* Balanced accuracy: **36.7%**
* Macro F1: **34.4%**

For binary A+ versus A− classification:

* Accuracy: **86.7%**
* Majority-class baseline: **86.7%**
* Balanced accuracy: **50.0%**
* Macro F1: **46.4%**

Both A− samples were predicted as A+, indicating that the binary model did not demonstrate meaningful predictive signal for the A− group under this validation strategy.

These results show that apparent cell-level predictive performance does not necessarily generalize when biological samples are held out.

## Overall Conclusion

The analysis revealed substantial heterogeneity in cell-type composition across Alzheimer's pathology states. Inhibitory-neuron abundance showed the strongest expl

