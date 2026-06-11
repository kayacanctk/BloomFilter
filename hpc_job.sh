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
 
echo "HPC Benchmark completed. Results saved."
