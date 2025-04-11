# Benchmark Dataset Creation: Reproducible Step-by-Step Workflow

---

## Step 0: Dataset and Directory Setup

### Datasets Used:
Gold standard assemblies were downloaded from the following CAMI II Toy Human Microbiome Project body sites:

- [Airways](https://openstack.cebitec.uni-bielefeld.de:8080/swift/v1/CAMI_Airways)
- [Gastrointestinal tract](https://openstack.cebitec.uni-bielefeld.de:8080/swift/v1/CAMI_Gastrointestinal_tract)
- [Oral cavity](https://openstack.cebitec.uni-bielefeld.de:8080/swift/v1/CAMI_Oral)
- [Skin](https://openstack.cebitec.uni-bielefeld.de:8080/swift/v1/CAMI_Skin)
- [Urogenital tract](https://openstack.cebitec.uni-bielefeld.de:8080/swift/v1/CAMI_Urogenital_tract)

Each dataset was placed in a corresponding subdirectory (e.g., `airways/`, `gastro_comp/`, etc.)

---

## Step 1: ORF Prediction with Prodigal

```bash
prodigal -i gsa.fa -a gsa_orfs.faa -d gsa_orfs.fna -o gsa_orfs.gff -p single
```

Run once per dataset (Airways, Gastrointestinal, etc.).

---

## Step 2: Align Predicted Proteins to UniRef90

Use DIAMOND with the prebuilt UniRef90 database:

```bash
diamond blastp \
  -q gsa_orfs.faa \
  -d path/to/uniref90-2021_03.dmnd \
  -o diamond_hits_uniref90.tsv \
  -f 6 qseqid sseqid pident length qcovhsp scovhsp evalue bitscore \
  --evalue 1e-5 \
  --max-target-seqs 1 \
  --threads 16
```

---

## Step 3: EC Mapping and Post-Filtering

### Files:
- `diamond_hits_uniref90.tsv`
- `uniref90_to_ec.tsv` (UniRef90 ID to EC mapping file)

### Python Script (`ec_map.py`):
```python
# Filters DIAMOND hits and maps UniRef90 IDs to EC numbers
...
```
Run it per dataset to generate `orf_ec_annotations.tsv`.

---

## Step 4: Generate Paired Sequence and Label Files

### Python Script (`gen_benchmark.py`):
```python
# Matches EC-labeled ORFs to nucleotide sequences from Prodigal output
# Produces: <site>_benchmark.fasta and <site>_benchmark.label
...
```



