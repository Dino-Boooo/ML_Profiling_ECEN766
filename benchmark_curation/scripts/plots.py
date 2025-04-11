#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# === Load input files ===
diamond_file = "diamond_hits_uniref90.tsv"
mapping_file = "uniref90_to_ec.tsv"

cols = [
    "qseqid", "sseqid", "pident", "length", "qcovhsp", "scovhsp",
    "evalue", "bitscore"
]

df = pd.read_csv(diamond_file, sep="\t", names=cols)
map_df = pd.read_csv(mapping_file, sep="\t", names=["sseqid", "ec_number"])
map_df["sseqid"] = map_df["sseqid"].str.strip()

# === Merge for EC annotation ===
merged = pd.merge(df, map_df, on="sseqid", how="left")

# === Apply HUMAnN-style filters ===
filtered = merged[
    (merged["pident"] >= 90.0) &
    (merged["qcovhsp"] >= 80.0) &
    (merged["scovhsp"] >= 80.0)
]

# === Plot 1: Bitscore distribution before and after filtering ===
plt.figure()
sns.histplot(df["bitscore"], kde=True, color="gray", label="Before Filter")
sns.histplot(filtered["bitscore"], kde=True, color="blue", label="After Filter")
plt.title("Bitscore Distribution")
plt.xlabel("Bitscore")
plt.legend()
plt.savefig("bitscore_distribution.png")

# === Plot 2: Percent identity distribution ===
plt.figure()
sns.histplot(df["pident"], kde=True, bins=50)
plt.title("Percent Identity (pident) Distribution")
plt.xlabel("Percent Identity")
plt.savefig("pident_distribution.png")

# === Plot 3: Query coverage vs Subject coverage ===
plt.figure()
sns.scatterplot(data=df, x="qcovhsp", y="scovhsp", alpha=0.3)
plt.title("Query vs Subject Coverage")
plt.xlabel("Query Coverage (%)")
plt.ylabel("Subject Coverage (%)")
plt.savefig("coverage_scatter.png")

# === Plot 4: ORFs with and without EC annotations ===
ec_annotated = merged["ec_number"].notna().sum()
ec_unannotated = merged["ec_number"].isna().sum()
plt.figure()
sns.barplot(x=["Annotated", "Unannotated"], y=[ec_annotated, ec_unannotated])
plt.title("ORF EC Annotation Status")
plt.ylabel("Number of ORFs")
plt.savefig("ec_annotation_status.png")

# === Plot 5: EC frequency (Top 20) ===
top_ec = merged["ec_number"].value_counts().dropna().head(20)
plt.figure()
top_ec.plot(kind="bar")
plt.title("Top 20 EC Numbers")
plt.ylabel("Count")
plt.xticks(rotation=90)
plt.tight_layout()
plt.savefig("top20_ec_numbers.png")

# === Plot 6: Alignment length distribution ===
plt.figure()
sns.histplot(df["length"], bins=50, kde=True)
plt.title("Sequence Alignment Length Distribution")
plt.xlabel("Alignment Length")
plt.savefig("alignment_length_distribution.png")

print("All plots saved as PNG files.")

