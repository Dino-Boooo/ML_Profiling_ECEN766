#!/bin/bash
#SBATCH --export=NONE
#SBATCH --job-name=dmnd_gastro
#SBATCH --time=0-08:00:00
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=48
#SBATCH --mem=300G
#SBATCH --output=stdout.%x.%j
#SBATCH --error=stderr.%x.%j

module load GCC/13.2.0
module load DIAMOND/2.1.9

# Start resource tracking
jobstats &

# File paths
ORF_FASTA="gastro/gsa_orfs.faa"
DIAMOND_DB="/scratch/user/jonathanturck/ecen776/benchmark_curation/diamond/uniref90-2021_03.dmnd"
OUTPUT_FILE="gastro/diamond_hits_uniref90.tsv"

# Run DIAMOND BLASTP alignment
diamond blastp \
  -q "$ORF_FASTA" \
  -d "$DIAMOND_DB" \
  -o "$OUTPUT_FILE" \
  -f 6 qseqid sseqid pident length qcovhsp scovhsp evalue bitscore \
  --max-target-seqs 1 \
  --sensitive \
  --threads 48

# Stop jobstats and generate plots/logs
jobstats
