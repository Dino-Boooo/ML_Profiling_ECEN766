# Benchmarking Transformer-Based Metagenomic Functional Profiling: A Comparison with Alignment Methods
This repository contains code and data to evaluate DeepECtransformer, a transformer-based deep learning model, for metagenomic functional annotation. We benchmark its performance against traditional alignment-based tools like HUMAnN3 and ML-based methods like Carnelian, using both clean validation data and real-world metagenomic benchmarking sets.
## Problem Statement
## Datasets
The validation set we will be using is the same set used by Carnelian. This set is comprised of 8227 proteins with 2200 unique labels. Then we will be using a benchmark set that comprises... 
## Models
The model we are evaluating is the DeepECtranformer. This model was trained on a uniprot dataset comprised of amino acid sequences of 22 million enzymes, covering 2802 EC numbers.
- Example to run DeepECtransformer (takes < 1 min)

        python run_deepectransformer.py -i ./example/mdh_ecoli.fa -o ./example/results -g cpu -b 128 -cpu 2
        python run_deepectransformer.py -i ./example/mdh_ecoli.fa -o ./example/results -g cuda:3 -b 128 -cpu 2
