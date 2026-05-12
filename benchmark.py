import time
import random
import urllib.request
import os
from bloom_filter import BloomFilter

# 1. NOMINAL DATA (Unstructured Text)
def get_common_english_words(limit):
    """Downloads a list of the most common English words (Nominal Text Data)."""
    file_path = "common_english.txt"
    if not os.path.exists(file_path):
        print("Downloading Nominal Data (Common English Words)...")
        url = "https://raw.githubusercontent.com/frekwencja/most-common-words-multilingual/main/data/wordfrequency.info/en.txt"
        urllib.request.urlretrieve(url, file_path)
    
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        words = f.read().splitlines()
    random.shuffle(words) 
    return words[:limit]

def generate_dna_sequences(limit, length=20):
    """Generates synthetic DNA sequences (Structured Nominal Data)."""
    print(f"Generating {limit} nominal data points (DNA sequences)...")
    bases = ['A', 'C', 'G', 'T']
    
    return [''.join(random.choices(bases, k=length)) for i in range(limit)]

def generate_numerical_data(limit):
    """Generates massive random integers to represent Numerical Data (e.g., Bank IDs)."""
    print(f"Generating {limit} numerical data points (Random IDs)...")
    return [random.randint(10000000, 99999999) for _ in range(limit)]

def run_benchmark(data_list, dataset_name):
    """Runs the insertion and search tests and prints out the timing."""
    test_sizes = [10000, 50000, 100000, 200000] 
    
    print(f"\n{'='*45}")
    print(f"  STARTING BENCHMARK: {dataset_name.upper()}")
    print(f"{'='*45}")
    
    for size in test_sizes:
        if size > len(data_list):
            print(f"Warning: Not enough data to test size {size}. Skipping.")
            break
            
        test_data = data_list[:size]
        
        bf = BloomFilter(expected_items=size, fp_rate=0.05)
        
        start_time = time.time()
        for item in test_data:
            bf.add(item)
        insert_time = time.time() - start_time
        
        start_time = time.time()
        for item in test_data:
            bf.check(item)
        search_time = time.time() - start_time
        
        print(f"Size: {size:<7} | Insert: {insert_time:.4f} sec | Search: {search_time:.4f} sec")

if __name__ == "__main__":

    MAX_LIMIT = 200000
    
    nominal_text_data = get_common_english_words(MAX_LIMIT)
    nominal_pattern_data = generate_dna_sequences(MAX_LIMIT)
    numerical_data = generate_numerical_data(MAX_LIMIT)
    
    run_benchmark(nominal_text_data, "Nominal Data (Common English)")
    run_benchmark(nominal_pattern_data, "Nominal Data (DNA Sequences)")
    run_benchmark(numerical_data, "Numerical Data (Random IDs)")