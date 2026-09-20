import argparse
import numpy as np
import pandas as pd
import scanpy as sc

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    f1_score,
    confusion_matrix,
    classification_report,
)


# ============================================================
# Configuration
# ============================================================

N_PCA_COMPONENTS = 5
MAX_ITER = 5000
C_VALUE = 1.0


# ============================================================
# Command-line argument
# ============================================================

parser = argparse.ArgumentParser(
    description=(
        "Sample-level leave-one-sample-out validation "
        "of Alzheimer pathology classification"
    )
)

parser.add_argument(
    "--data",
    required=True,
    help="Path to the GSE243292 .h5ad file"
)

args = parser.parse_args()

DATA_PATH = args.data


# ============================================================
# Load data
# ============================================================

print("Loading dataset...")

adata = sc.read_h5ad(DATA_PATH)

print(f"Cells: {adata.n_obs:,}")
print(f"Genes: {adata.n_vars:,}")


# ============================================================
# Normalize and log-transform
# ============================================================

print("\nNormalizing expression...")

sc.pp.normalize_total(
    adata,
    target_sum=1e4
)

sc.pp.log1p(adata)


# ============================================================
# Aggregate cells within each biological sample
# ============================================================

print("\nAggregating cells by biological sample...")

sample_ids = adata.obs["sampleID"].unique()

sample_expression = []

for sample_id in sample_ids:

    mask = (
        adata.obs["sampleID"].values == sample_id
    )

    X_sample = adata.X[mask]

    if hasattr(X_sample, "toarray"):
        X_sample = X_sample.toarray()

    X_sample_mean = np.asarray(
        X_sample
    ).mean(axis=0)

    sample_expression.append(
        X_sample_mean
    )

sample_expression = pd.DataFrame(
    sample_expression,
    index=sample_ids,
    columns=adata.var_names
)

print(
    f"Sample-level expression matrix: "
    f"{sample_expression.shape[0]} samples × "
    f"{sample_expression.shape[1]} genes"
)


# ============================================================
# Build sample-level pathology labels
# ============================================================

sample_labels = (
    adata.obs[
        ["sampleID", "atscore"]
    ]
    .drop_duplicates("sampleID")
    .set_index("sampleID")["atscore"]
)

# Binary classification:
#
# A-T-  -> A-
# A+T-  -> A+
# A+T+  -> A+

binary_labels = sample_labels.map({
    "A-T-": "A-",
    "A+T-": "A+",
    "A+T+": "A+",
})

binary_labels = binary_labels.loc[
    sample_expression.index
]


print("\nPathology distribution:")
print(
    binary_labels.value_counts()
)


# ============================================================
# Prepare feature matrix
# ============================================================

X = sample_expression.values
y = binary_labels.values

samples = sample_expression.index.values


# ============================================================
# Leave-one-sample-out validation
# ============================================================

true_labels = []
pred_labels = []
pred_probabilities = []
pred_samples = []


for i in range(len(samples)):

    # --------------------------------------------------------
    # Hold out exactly one biological sample
    # --------------------------------------------------------

    test_idx = i

    train_idx = np.delete(
        np.arange(len(samples)),
        i
    )

    X_train = X[train_idx]
    X_test = X[
        test_idx:test_idx + 1
    ]

    y_train = y[train_idx]
    y_test = y[
        test_idx:test_idx + 1
    ]


    # --------------------------------------------------------
    # Standardization
    #
    # Fit ONLY on training samples
    # --------------------------------------------------------

    scaler = StandardScaler()

    X_train_scaled = scaler.fit_transform(
        X_train
    )

    X_test_scaled = scaler.transform(
        X_test
    )


    # --------------------------------------------------------
    # PCA
    #
    # Fit ONLY on training samples
    # --------------------------------------------------------

    n_components = min(
        N_PCA_COMPONENTS,
        X_train_scaled.shape[0] - 1
    )

    pca = PCA(
        n_components=n_components
    )

    X_train_pca = pca.fit_transform(
        X_train_scaled
    )

    X_test_pca = pca.transform(
        X_test_scaled
    )


    # --------------------------------------------------------
    # Logistic regression
    # --------------------------------------------------------

    model = LogisticRegression(
        max_iter=MAX_ITER,
        C=C_VALUE,
        class_weight="balanced"
    )

    model.fit(
        X_train_pca,
        y_train
    )


    # --------------------------------------------------------
    # Prediction
    # --------------------------------------------------------

    prediction = model.predict(
        X_test_pca
    )[0]

    class_index = list(
        model.classes_
    ).index("A+")

    probability = model.predict_proba(
        X_test_pca
    )[0, class_index]


    # --------------------------------------------------------
    # Store result
    # --------------------------------------------------------

    true_labels.append(
        y_test[0]
    )

    pred_labels.append(
        prediction
    )

    pred_probabilities.append(
        probability
    )

    pred_samples.append(
        samples[i]
    )


# ============================================================
# Convert results to arrays
# ============================================================

true_labels = np.array(
    true_labels
)

pred_labels = np.array(
    pred_labels
)

pred_probabilities = np.array(
    pred_probabilities
)


# ============================================================
# Evaluation
# ============================================================

accuracy = accuracy_score(
    true_labels,
    pred_labels
)

balanced_accuracy = balanced_accuracy_score(
    true_labels,
    pred_labels
)

macro_f1 = f1_score(
    true_labels,
    pred_labels,
    average="macro"
)

cm = confusion_matrix(
    true_labels,
    pred_labels,
    labels=["A-", "A+"]
)


# Majority-class baseline
majority_class = pd.Series(
    y
).value_counts().index[0]

majority_baseline = np.mean(
    y == majority_class
)


# ============================================================
# Print results
# ============================================================

print("\n" + "=" * 60)
print("A+ vs A- LEAVE-ONE-SAMPLE-OUT VALIDATION")
print("=" * 60)

print(
    f"\nAccuracy:            {accuracy:.4f}"
)

print(
    f"Balanced accuracy:   {balanced_accuracy:.4f}"
)

print(
    f"Macro F1:            {macro_f1:.4f}"
)

print(
    f"Majority baseline:   {majority_baseline:.4f}"
)


print("\nConfusion matrix:")
print("Rows = true labels")
print("Columns = predicted labels")
print("          A-    A+")

print(
    f"A-       {cm[0, 0]:3d}   {cm[0, 1]:3d}"
)

print(
    f"A+       {cm[1, 0]:3d}   {cm[1, 1]:3d}"
)


print("\nClassification report:")

print(
    classification_report(
        true_labels,
        pred_labels,
        labels=["A-", "A+"],
        zero_division=0
    )
)


# ============================================================
# Individual sample predictions
# ============================================================

print("\nIndividual predictions:")

results_df = pd.DataFrame({
    "sampleID": pred_samples,
    "true_label": true_labels,
    "predicted_label": pred_labels,
    "P_A_positive": pred_probabilities,
})

print(
    results_df.to_string(
        index=False
    )
)


# ============================================================
# Save results
# ============================================================

results_df.to_csv(
    "sample_level_LOSO_predictions.csv",
    index=False
)

summary_df = pd.DataFrame({
    "metric": [
        "accuracy",
        "balanced_accuracy",
        "macro_f1",
        "majority_baseline"
    ],
    "value": [
        accuracy,
        balanced_accuracy,
        macro_f1,
        majority_baseline
    ],
})

summary_df.to_csv(
    "sample_level_LOSO_metrics.csv",
    index=False
)


print("\nSaved:")
print(
    "  sample_level_LOSO_predictions.csv"
)
print(
    "  sample_level_LOSO_metrics.csv"
)
