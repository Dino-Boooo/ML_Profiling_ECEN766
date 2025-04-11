#!/usr/bin/env python3

from Bio import SeqIO
import pandas as pd

# === Config ===
orf_ec_file = "orf_ec_annotations.tsv"
fasta_input = "gsa_orfs.faa"  # Your Prodigal FAA file
fasta_output = "seq.fasta"
label_output = "seq.label"

# === Step 1: Load ORF to EC mapping ===
orf2ec = pd.read_csv(orf_ec_file, sep="\t", names=["qseqid", "ec_number"])
orf2ec_dict = dict(zip(orf2ec["qseqid"], orf2ec["ec_number"]))

# === Step 2: Filter and write matching sequences ===
with open(fasta_output, "w") as fasta_out, open(label_output, "w") as label_out:
    count = 0
    for record in SeqIO.parse(fasta_input, "fasta"):
        if record.id in orf2ec_dict:
            SeqIO.write(record, fasta_out, "fasta")
            label_out.write(orf2ec_dict[record.id] + "\n")
            count += 1

print(f" Wrote {count} EC-labeled sequences to '{fasta_output}' and '{label_output}'")

