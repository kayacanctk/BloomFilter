# BloomFilter_CDS_Project
Bloom filter project tests whether an item is a member of a set using a small amount of memory. It guarantees no false negatives: if the filter reports that an item is not in the set, it is definitely not in the set. It allows a small, controlled rate of false positives: if the filter reports that an item is in the set, it may occasionally be wrong.

## Team Members
* Sefa Kayacan Citak
* Maryna Poberezhna

## Description
This repository implements a Bloom filter using an object-oriented approach and benchmarks its performance on the VSC Wice HPC cluster. The data structure is built from scratch, with a family of k hash functions derived from hashlib.md5. The benchmark measures insert and search time across three different data profiles and increasing dataset sizes.

## Getting Started

### Project Structure
* `bloom_filter.py`: The core implementation of the Bloom Filter data structure using optimized hash functions.
* `benchmark.py`: The main testing script that generates synthetic data, loads external datasets, and measures performance metrics.
* `hpc_job.sh`: SLURM batch script for submitting the benchmark to the Wice cluster.
* `benchmark_hpc_output.txt`: Captured output of the benchmark run on Wice.
* `words_dictionary.json`: Dataset of ~370,000 English words used for the text benchmark. Included in the repository; keep it in the same directory as `benchmark.py`.

### Datasets Evaluated
The benchmarking suite tests the Bloom Filter against three distinct data profiles, scaling up to 200,000 items:
1. **Nominal Data (Unstructured Text):** Real English words loaded from `words_dictionary.json`.
2. **Nominal Data (Structured Patterns):** Synthetically generated 20-character DNA sequences (A, C, G, T).
3. **Numerical Data:** Random 8-digit integer IDs.

`words_dictionary.json` is the common ~370k-word English dictionary (dwyl/english-words). Add the exact download link you used here so the dataset is reproducible.

## Implementation Notes
* **Hash family:** `k` hash functions are simulated by seeding the input with an index (`item_i`) before hashing with md5, then reducing modulo the bit-array size `m`.
* **Sizing:** the bit-array size `m` and hash count `k` are derived from the expected item count `n` and the target false positive rate `p`:
  * `m = -(n * ln p) / (ln 2)^2`
  * `k = (m / n) * ln 2`
* The target false positive rate used throughout the benchmark is `p = 0.05`.

## Dependencies
* **Runtime:** Python 3.13, loaded on Wice with `module load Python`.
* **Standard library only:** `math`, `hashlib` (in `bloom_filter.py`); `time`, `random`, `json` (in `benchmark.py`).
* No third-party packages are required by the current implementation.
## Running on the HPC

1. Transfer the project into your VSC data/scratch directory, either with `git clone <repo-url>` (if the login node has outbound internet) or `scp`.
2. Make sure `words_dictionary.json` is in the same directory as `benchmark.py`.
3. (Optional) Edit `MAX_LIMIT` in `benchmark.py` to change the largest dataset size (default `200000`).
4. Submit the job to the queue:

```bash
sbatch hpc_job.sh
```

The job script (`hpc_job.sh`):

```bash
#!/bin/bash -l
#SBATCH --job-name=bloom_benchmark
#SBATCH --account=lp_h_ds_students
#SBATCH --cluster=wice
#SBATCH --time=00:15:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=2G
#SBATCH --output=benchmark_hpc_output.txt

echo "Starting HPC Benchmark on WICE..."
 
module load Python
 
pip install --user matplotlib
 
python benchmark.py
python experiments.py
 
echo "HPC Benchmark completed. Results saved."
```

Results are written to `benchmark_hpc_output.txt`.

## Results

Benchmarks were run on Wice (1 node, 1 task, 1 CPU, 2 GB RAM) at a target false
positive rate of `p = 0.05`. Times are in seconds.

| Items   | Words insert | Words search | DNA insert | DNA search | IDs insert | IDs search |
|---------|--------------|--------------|------------|------------|------------|------------|
| 10,000  | 0.0464       | 0.0466       | 0.0451     | 0.0455     | 0.0460     | 0.0464     |
| 50,000  | 0.2332       | 0.2350       | 0.2279     | 0.2302     | 0.2326     | 0.2338     |
| 100,000 | 0.4630       | 0.4721       | 0.4616     | 0.4672     | 0.4631     | 0.4686     |
| 200,000 | 0.9410       | 0.9597       | 0.9300     | 0.9365     | 0.9281     | 0.9502     |

## Conclusion

The benchmark results from the Wice HPC cluster highlight the efficiency and stability of our custom Bloom Filter implementation.

* When testing our maximum capacity of 200,000 items, both insertion and search operations were completed in under a second (averaging around 0.94s and 0.95s, respectively). Most significant is the consideration of the time required for processing the data sets of varying size (10k, 50k, 100k, and 200k): the total processing time scales linearly, from approximately 0.046s to 0.94s. This indicates that the time complexity to process a single item is constant, $O(k)$, regardless of the number of items in the filter.

* We also observed that the filter's performance is practically independent of the data structure. The execution times were almost identical whether the algorithm was hashing unstructured English words, 20-character DNA sequences, or numerical IDs.

* In the end, our implementation turns out to be exactly what we expected: it is highly memory efficient and fast to deal with large data sets, and yields a small but controlled false positive rate of 5%, which is a significant improvement in data pipelines.

## Support
For cluster configuration and scaling issues, please write a comment under a relevant pull request.
