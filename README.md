# Benchmarking Transformer-Based Metagenomic Functional Profiling: A Comparison with Alignment Methods
This repository contains code and data to evaluate DeepECtransformer, a transformer-based deep learning model, for metagenomic functional annotation. We benchmark its performance against traditional alignment-based tools like HUMAnN3 and ML-based methods like Carnelian, using both clean validation data and real-world metagenomic benchmarking sets.
## Problem Statement
There is a lack of evidence for the real-world effectiveness of transformer-based models for full metagenome functional annotation. Rigorous benchmarking against well-established alignment-based tools is therefore essential to determine whether these newer methods can reliably complement, or even surpass, traditional approaches in functional profiling.

## Datasets
The validation set we will be using is the same set used by Carnelian. This set is comprised of 7884 proteins with 2200 unique labels. Then we will be using a benchmark set that comprises of: 
- 109,559 Airways sequences
- 8,006 Gastrointestinal sequences
- 18,865 Oral sequences
- 109,230 Skin sequences
- 5,859 Urogenital sequences
## Models
The model we are evaluating is the DeepECtranformer. This model was trained on a uniprot dataset comprised of amino acid sequences of 22 million enzymes, covering 2802 EC numbers.
- Example to run DeepECtransformer (takes < 1 min)

        python run_deepectransformer.py -i ./example/mdh_ecoli.fa -o ./example/results -g cpu -b 128 -cpu 2
        python run_deepectransformer.py -i ./example/mdh_ecoli.fa -o ./example/results -g cuda:3 -b 128 -cpu 2

## Benchmark Set: Zenodo
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.15192200.svg)](https://doi.org/10.5281/zenodo.15192200)

