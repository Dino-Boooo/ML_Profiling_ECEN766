#!/usr/bin/env python3

import pandas as pd

# === Config ===
diamond_file = "diamond_hits_uniref90.tsv"
mapping_file = "uniref90_to_ec.tsv"  # Converted from ec2uniref90.tsv
output_file = "orf_ec_annotations.tsv"

# === Step 1: Load DIAMOND hits ===
cols = [
    "qseqid", "sseqid", "pident", "length", "qcovhsp", "scovhsp",
    "evalue", "bitscore"
]
df = pd.read_csv(diamond_file, sep="\t", names=cols)

# === Step 2: Filter high-confidence hits (HUMAnN3 style) ===
filtered = df[
    (df["pident"] >= 90.0) &
    (df["qcovhsp"] >= 80.0) &
    (df["scovhsp"] >= 80.0)
]

# === Step 3: Load UniRef90 → EC mapping ===
map_df = pd.read_csv(mapping_file, sep="\t", names=["sseqid", "ec_number"])
map_df["sseqid"] = map_df["sseqid"].str.strip()

# === Step 4: Merge filtered hits with EC annotations ===
merged = pd.merge(filtered, map_df, on="sseqid", how="left")

# === Step 5: Drop entries without EC annotation ===
annotated = merged.dropna(subset=["ec_number"])

# === Step 6 (Optional): Keep best hit per ORF (qseqid) ===
# If you want to keep only the best scoring hit per ORF:
best_hits = annotated.sort_values("bitscore", ascending=False).drop_duplicates("qseqid")

# === Step 7: Output final ORF-to-EC mapping ===
best_hits[["qseqid", "ec_number"]].to_csv(output_file, sep="\t", index=False)

print(f"ORF to EC mapping complete. Output written to {output_file}")

