#!/bin/bash
#SBATCH --job-name=bloom_benchmark
#SBATCH --time=00:15:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=2G
#SBATCH --output=benchmark_hpc_output.txt

echo "Starting HPC Benchmark..."

python benchmark.py

echo "HPC Benchmark completed. Results saved."