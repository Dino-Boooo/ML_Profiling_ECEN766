import os
import matplotlib.pyplot as plt
import seaborn as sns

# === Config ===
label_files = {
    "Airways": "airways_benchmark.label",
    "Gastrointestinal": "gastro_benchmark.label",
    "Oral": "oral_benchmark.label",
    "Skin": "skin_benchmark.label",
    "Urogenital": "uro_benchmark.label"
}

# === Tally ECs ===
site_unique_ecs = {}
all_ecs = set()

for site, filepath in label_files.items():
    with open(filepath) as f:
        ecs = {line.strip() for line in f if line.strip()}
        site_unique_ecs[site] = ecs
        all_ecs.update(ecs)

# === Count unique ECs ===
site_counts = {site: len(ecs) for site, ecs in site_unique_ecs.items()}
site_counts["Total Unique"] = len(all_ecs)

# === Plot ===
sns.set(style="whitegrid")
plt.rcParams.update({
    'font.size': 16,
    'axes.labelweight': 'bold',
    'axes.titlesize': 20,
    'axes.titleweight': 'bold',
    'xtick.labelsize': 14,
    'ytick.labelsize': 14
})

plt.figure(figsize=(10, 6))
colors = ["mediumseagreen" if k != "Total Unique" else "goldenrod" for k in site_counts]
bars = plt.bar(site_counts.keys(), site_counts.values(), color=colors)

# Add value labels
for bar in bars:
    height = bar.get_height()
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        height + (0.01 * height),
        f"{height:,}",
        ha='center',
        va='bottom',
        fontweight='bold'
    )

# === Labeling ===
plt.ylabel("Number of Unique ECs", fontweight="bold")
plt.title("Unique EC Numbers by Body Site and Combined", fontweight="bold")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

# Save and show
plt.savefig("unique_ecs_by_site_and_total.png", dpi=300)
plt.show()

