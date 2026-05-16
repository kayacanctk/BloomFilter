# BloomFilter_CDS_Project
The purpose of this project is to implement a space-efficient probabilistic data structure of a bloom filter that checks if an item belongs to a list, using a small amount of computer memory. Namely, if it is not on the list, it will definitely not be on the list. However, if an item is mentioned to be in the list, there is still a small chance that it could be a False Positive.

## Description
The Bloom filter, a probability data structure used to determine if an entry is related to a set, is implemented in this repository. The project involves constructing the data structure from the beginning into a Python, assessing various hash function families, and using an HPC infrastructure to benchmark its performance (time and space complexity).

## Getting Started

### Dependencies
Since this project runs on HPC supercomputer, it relies on an isolated environment to manage dependencies.
#### Platform Environment: Supercomputer Cluster
#### Environment Manager: Conda
#### Runtime Environment: Python 3.8+
#### Libraries and Modules: Math, Hashlib, Time, Random, JSON, Bloom_filter, BloomFilter
#### Dataset: words_dictionary.json

## Installing
You can pull or transfer the program files into your target HPC.
Either clone it directly into your designated space via 'git clone' or you can deploy the entire project architecture via 'scp' directly to your cluster directory.
The first method is preferred if your cluster nodes maintain outbound internet clearance. Since it allows a supercomputer node to connect to the external internet.


## Executing a program
1. Log into the supercomputer node using terminal
2. Initialise the Conda environment
3. Clone the project from git
4. Do a batch submission for a large MAX_LIM size

E.g.:
`#!/bin/bash -l
#SBATCH --job-name=bloom_benchmark
#SBATCH --account=lp_h_ds_students
#SBATCH --cluster=wice
#SBATCH --time=00:15:00
#SBATCH --nodes=1
#SBATCH --ntasks=1`

5. Submit it to the HPC queue:

E.g:`sbatch submit_job.sh`

## Team Members
* Sefa Kayacan Citak
* Maryna Poberezhna

## Support
For cluster configuration and scaling issues, please write a comment under a relevant pull request.
