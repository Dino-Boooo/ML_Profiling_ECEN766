#!/bin/bash
#SBATCH --export=NONE
#SBATCH --job-name=build_dmndb
#SBATCH --time=0-10:00:00
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=48
#SBATCH --mem=300G
#SBATCH --output=stdout.%x.%j
#SBATCH --error=stderr.%x.%j

module load GCC/13.2.0
module load DIAMOND/2.1.9

# Input FASTA and output prefix
FASTA="/scratch/data/bio/uniref/uniref90-2021_03.fasta"
OUT_PREFIX="/scratch/user/jonathanturck/ecen776/benchmark_curation/diamond"

# Build the DIAMOND database
diamond makedb --in "$FASTA" -d "$OUT_PREFIX" --threads 48 --verbose

echo "DIAMOND database created at ${OUT_PREFIX}.dmnd"
