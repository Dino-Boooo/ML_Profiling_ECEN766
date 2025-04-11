#!/usr/bin/env python3

import os
import matplotlib.pyplot as plt

# Define top-level dataset directories
body_sites = {
    "airways": "airways/gsa_orfs.faa",
    "gastrointestinal": "gastro_comp/gsa_orfs.faa",
    "oral": "oral/gsa_orfs.faa",
    "skin": "skin/gsa_orfs.faa",
    "urogenital": "uro_comp/gsa_orfs.faa"
}

orf_counts = {}

# Count ORFs per site
for site, faa_path in body_sites.items():
    count = 0
    if os.path.isfile(faa_path):
        with open(faa_path) as f:
            for line in f:
                if line.startswith(">"):
                    count += 1
        orf_counts[site.capitalize()] = count
    else:
        print(f"Missing file for {site}: {faa_path}")

# Plot with bigger, bold fonts
plt.figure(figsize=(10, 6))
bars = plt.bar(orf_counts.keys(), orf_counts.values())

plt.ylabel("Number of Predicted ORFs", fontsize=14, fontweight='bold')
plt.title("Number of Predicted ORFs by Body Site", fontsize=16, fontweight='bold')
plt.xticks(rotation=45, fontsize=12, fontweight='bold')
plt.yticks(fontsize=12, fontweight='bold')

# Optionally make bar labels bold too
for bar in bars:
    height = bar.get_height()
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        height,
        f"{height:,}",
        ha='center',
        va='bottom',
        fontsize=12,
        fontweight='bold'
    )

plt.tight_layout()
plt.savefig("orf_counts_by_site.png", dpi=300)
print("Plot saved as orf_counts_by_site.png")

