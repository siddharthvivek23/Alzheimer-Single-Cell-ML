import argparse

import numpy as np
import pandas as pd
import scanpy as sc
import matplotlib.pyplot as plt

from scipy.stats import spearmanr, mannwhitneyu
from statsmodels.stats.multitest import multipletests


# ============================================================
# Command-line argument
# ============================================================

parser = argparse.ArgumentParser(
    description=(
        "Analyze cell-type composition across "
        "Alzheimer's pathology states"
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
# Build sample-level pathology labels
# ============================================================

sample_labels = (
    adata.obs[
        ["sampleID", "atscore"]
    ]
    .drop_duplicates("sampleID")
    .set_index("sampleID")["atscore"]
)

pathology_scores = sample_labels.map({
    "A-T-": 0,
    "A+T-": 1,
    "A+T+": 2
})


# ============================================================
# Calculate cell-type composition within each sample
# ============================================================

print("\nCalculating cell-type composition...")

composition = pd.crosstab(
    adata.obs["sampleID"],
    adata.obs["final_celltype"],
    normalize="index"
) * 100

composition["pathology"] = pathology_scores.loc[
    composition.index
]


print("\nSample-level composition:")
print(
    composition.to_string()
)


# ============================================================
# Correlation between cell-type composition
# and ordinal pathology state
# ============================================================

cell_types = [
    cell_type
    for cell_type in adata.obs["final_celltype"].unique()
    if cell_type in composition.columns
]

correlation_results = []

for cell_type in cell_types:

    rho, p_value = spearmanr(
        composition[cell_type],
        composition["pathology"]
    )

    correlation_results.append({
        "cell_type": cell_type,
        "rho": rho,
        "p_value": p_value
    })


correlation_results = pd.DataFrame(
    correlation_results
).sort_values(
    "p_value"
)


# ============================================================
# Multiple-testing correction
# ============================================================

p_values = correlation_results["p_value"].values

_, p_bonferroni, _, _ = multipletests(
    p_values,
    method="bonferroni"
)

_, p_fdr, _, _ = multipletests(
    p_values,
    method="fdr_bh"
)

correlation_results["p_bonferroni"] = p_bonferroni
correlation_results["p_fdr"] = p_fdr


print("\nCell-type/pathology correlations:")
print(
    correlation_results.to_string(index=False)
)


# ============================================================
# A+T- vs A+T+ comparison for inhibitory neurons
# ============================================================

if "In" in composition.columns:

    a_plus_t_minus = composition.loc[
        composition["pathology"] == 1,
        "In"
    ].values

    a_plus_t_plus = composition.loc[
        composition["pathology"] == 2,
        "In"
    ].values

    u_stat, mw_p = mannwhitneyu(
        a_plus_t_minus,
        a_plus_t_plus,
        alternative="greater"
    )

    print(
        "\nA+T- inhibitory neuron percentages:"
    )
    print(
        np.round(a_plus_t_minus, 3)
    )

    print(
        "\nA+T+ inhibitory neuron percentages:"
    )
    print(
        np.round(a_plus_t_plus, 3)
    )

    print(
        f"\nMann-Whitney U = {u_stat:.3f}"
    )

    print(
        f"Mann-Whitney p-value = {mw_p:.4f}"
    )


# ============================================================
# Save results
# ============================================================

composition.to_csv(
    "sample_cell_type_composition.csv"
)

correlation_results.to_csv(
    "cell_type_pathology_correlations.csv",
    index=False
)


# ============================================================
# Plot inhibitory-neuron composition
# ============================================================

if "In" in composition.columns:

    groups = [
        (
            "A-T-",
            composition.loc[
                composition["pathology"] == 0,
                "In"
            ].values
        ),
        (
            "A+T-",
            composition.loc[
                composition["pathology"] == 1,
                "In"
            ].values
        ),
        (
            "A+T+",
            composition.loc[
                composition["pathology"] == 2,
                "In"
            ].values
        )
    ]

    fig, ax = plt.subplots(
        figsize=(8, 6)
    )

    rng = np.random.default_rng(42)

    for x, (label, values) in enumerate(groups):

        jitter = rng.uniform(
            -0.08,
            0.08,
            size=len(values)
        )

        ax.scatter(
            np.full(len(values), x) + jitter,
            values,
            s=70,
            alpha=0.85,
            edgecolor="black",
            linewidth=0.8
        )

        median = np.median(values)

        ax.hlines(
            median,
            x - 0.18,
            x + 0.18,
            linewidth=3
        )

    ax.set_xticks([0, 1, 2])

    ax.set_xticklabels([
        "A−T−",
        "A+T−",
        "A+T+"
    ])

    ax.set_xlabel(
        "Pathology group"
    )

    ax.set_ylabel(
        "Inhibitory neuron proportion (%)"
    )

    ax.set_title(
        "Inhibitory Neuron Proportion Across Pathology States"
    )

    ax.grid(
        axis="y",
        alpha=0.25
    )

    plt.tight_layout()

    plt.savefig(
        "inhibitory_neuron_pathology.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()


# ============================================================
# Completion message
# ============================================================

print("\nSaved:")
print(
    "  sample_cell_type_composition.csv"
)
print(
    "  cell_type_pathology_correlations.csv"
)

if "In" in composition.columns:
    print(
        "  inhibitory_neuron_pathology.png"
    )
