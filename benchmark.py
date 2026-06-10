"""Benchmarks for the Bloom filter: timing, false positive rate and compression."""
import time
import random
import json
import csv
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from bloom_filter import BloomFilter


def load_word_dataset(file_path, limit):
    """Loads the JSON dictionary and returns up to `limit` words."""
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    words = list(data.keys())
    return words[:min(limit, len(words))]


def generate_dna_sequences(limit, length=20):
    """Random DNA strings (structured nominal data)."""
    print(f"Generating {limit} DNA sequences...")
    bases = ["A", "C", "G", "T"]
    return ["".join(random.choices(bases, k=length)) for _ in range(limit)]


def generate_numerical_data(limit):
    """Random 8-digit IDs (numerical data)."""
    print(f"Generating {limit} numerical IDs...")
    return [random.randint(10000000, 99999999) for _ in range(limit)]


def save_csv(path, header, rows):
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)


def run_benchmark(data, name):
    """Times insert and search for growing sample sizes."""
    sizes = [10000, 50000, 100000, 200000]
    print(f"\n{'='*45}\n  {name.upper()}\n{'='*45}")
    rows = []
    for size in sizes:
        if size > len(data):
            print(f"Not enough data for size {size}, skipping.")
            break
        sample = data[:size]
        bf = BloomFilter(expected_items=size, fp_rate=0.05)

        start = time.time()
        for item in sample:
            bf.add(item)
        insert_time = time.time() - start

        start = time.time()
        for item in sample:
            bf.check(item)
        search_time = time.time() - start

        rows.append((size, insert_time, search_time))
        print(f"Size: {size:<7} | Insert: {insert_time:.4f} sec | Search: {search_time:.4f} sec")
    return rows


def false_positive_experiment(words, n_design=50000, fp_rate=0.05,
                              max_inserted=200000, step=5000, test_size=20000):
    insert_pool = words[:max_inserted]
    test_words = words[max_inserted:max_inserted + test_size]

    bf = BloomFilter(expected_items=n_design, fp_rate=fp_rate)
    m, k = bf.size, bf.hash_count
    print(f"\nExperiment 7 - filter built for {n_design} words, p={fp_rate} (m={m}, k={k})")

    rows = []
    added = 0
    for count in range(step, max_inserted + 1, step):
        for w in insert_pool[added:count]:
            bf.add(w)
        added = count

        hits = sum(1 for w in test_words if bf.check(w))
        empirical = hits / test_size
        theoretical = (1 - math.exp(-k * count / m)) ** k
        fill = bf.bits_set() / m
        rows.append((count, empirical, theoretical, fill))
        print(f"inserted {count:>6}: measured {empirical:.4f} | expected {theoretical:.4f}")
    return rows, n_design, fp_rate, m, k


def compression_experiment(fp_rates=(0.001, 0.005, 0.01, 0.05, 0.1, 0.25),
                           sizes=(10000, 50000, 100000, 200000), baseline_bits=64):

    by_p = []
    for p in fp_rates:
        bits_per_word = -math.log(p) / (math.log(2) ** 2)
        by_p.append((p, bits_per_word, baseline_bits / bits_per_word))
        print(f"p={p}: {bits_per_word:.2f} bits/word, "
              f"{baseline_bits / bits_per_word:.1f}x smaller than a {baseline_bits}-bit key")

    by_n = []
    for n in sizes:
        bf = BloomFilter(expected_items=n, fp_rate=0.05)
        size_kb = bf.size / 8 / 1024
        by_n.append((n, bf.size, bf.size / n, size_kb))
        print(f"n={n}: {bf.size} bits, {bf.size / n:.2f} bits/word, {size_kb:.1f} KB")

    return by_p, by_n


def plot_timing(timing):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    for name, rows in timing.items():
        sizes = [r[0] for r in rows]
        ax1.plot(sizes, [r[1] for r in rows], "o-", label=name)
        ax2.plot(sizes, [r[2] for r in rows], "o-", label=name)
    ax1.set(title="Insert time", xlabel="Number of items", ylabel="Seconds")
    ax2.set(title="Search time", xlabel="Number of items", ylabel="Seconds")
    for ax in (ax1, ax2):
        ax.grid(alpha=0.3)
        ax.legend()
    fig.tight_layout()
    fig.savefig("benchmark_timing.png", dpi=150)
    plt.close(fig)
 
 
def plot_false_positive(rows, n_design, fp_rate, m, k):
    counts = [r[0] for r in rows]
    plt.figure(figsize=(8, 5))
    plt.plot(counts, [r[1] for r in rows], "o-", label="Measured", color="tab:blue")
    plt.plot(counts, [r[2] for r in rows], "--", label="Expected", color="tab:orange")
    plt.axhline(fp_rate, color="grey", linestyle=":", label=f"Target p = {fp_rate}")
    plt.axvline(n_design, color="red", linestyle=":", label=f"Design size = {n_design}")
    plt.xlabel("Words inserted")
    plt.ylabel("False positive rate")
    plt.title(f"False positive rate vs words inserted (m={m}, k={k})")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig("fpr.png", dpi=150)
    plt.close()
 
 
def plot_compression(by_p, by_n):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    ax1.plot([r[0] for r in by_p], [r[1] for r in by_p], "o-", color="tab:blue")
    ax1.set_xscale("log")
    ax1.set(title="Bits per word vs p", xlabel="False positive rate (log)", ylabel="Bits per word")
    ax1.grid(alpha=0.3)
    ax2.plot([r[0] for r in by_n], [r[3] for r in by_n], "s-", color="tab:orange")
    ax2.set(title="Filter size vs n (p=0.05)", xlabel="Number of words", ylabel="Size (KB)")
    ax2.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig("compression.png", dpi=150)
    plt.close(fig)
 
 
if __name__ == "__main__":
    MAX_LIMIT = 200000
 
    # load a bit more than MAX_LIMIT so experiment 7 has spare words to use as a test set
    words = load_word_dataset("words_dictionary.json", MAX_LIMIT + 20000)
    dna = generate_dna_sequences(MAX_LIMIT)
    ids = generate_numerical_data(MAX_LIMIT)
 
    timing = {
        "English words": run_benchmark(words, "Nominal Data (English Words)"),
        "DNA sequences": run_benchmark(dna, "Nominal Data (DNA Sequences)"),
        "Random IDs": run_benchmark(ids, "Numerical Data (Random IDs)"),
    }
    plot_timing(timing)
 
    fp_rows, n_design, fp_rate, m, k = false_positive_experiment(words)
    plot_false_positive(fp_rows, n_design, fp_rate, m, k)
 
    by_p, by_n = compression_experiment()
    plot_compression(by_p, by_n)
