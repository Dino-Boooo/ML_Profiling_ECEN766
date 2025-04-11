#!/bin/bash
#SBATCH --export=NONE
#SBATCH --job-name=prodigal_airway
#SBATCH --time=0-02:00:00
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=48
#SBATCH --mem=300G
#SBATCH --output=stdout.%x.%j
#SBATCH --error=stderr.%x.%j

# Load Prodigal module (adjust as needed for your HPC environment)
module load GCCcore/12.3.0
module load prodigal/2.6.3

# Input and output paths
INPUT_FASTA="gsa.fa"                     # Your pooled gold standard contigs
OUTPUT_GFF="gsa_orfs.gff"               # Coordinates of predicted genes
OUTPUT_PROTEINS="gsa_orfs.faa"          # Predicted protein sequences
OUTPUT_NUCLEOTIDES="gsa_orfs.fna"       # Nucleotide sequences of ORFs

# Run Prodigal in "single genome" mode (works well for clean assemblies like this)
prodigal -i "$INPUT_FASTA" \
         -o "$OUTPUT_GFF" \
         -a "$OUTPUT_PROTEINS" \
         -d "$OUTPUT_NUCLEOTIDES" \
         -p single

echo "Prodigal completed on $INPUT_FASTA"

