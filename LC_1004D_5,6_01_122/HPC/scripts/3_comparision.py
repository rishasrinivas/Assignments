import multiprocessing

# Function to count variants in a chromosome
def count_variants_in_chrom(chrom):
    vcf = cyvcf2.VCF(vcf_path)
    count = sum(1 for v in vcf if v.CHROM == chrom)
    return chrom, count

# Get unique chromosomes
vcf = cyvcf2.VCF(vcf_path)
chromosomes = list(set(v.CHROM for v in vcf))

# Start timer
start_time = time.time()

# Run parallel analysis
with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
    results = pool.map(count_variants_in_chrom, chromosomes)

# End timer
hpc_time = time.time() - start_time

# Convert results to dict
hpc_variant_counts = dict(results)

# Save report
with open("results/reports/hpc_variant_counts.txt", "w") as f:
    for chrom, count in hpc_variant_counts.items():
        f.write(f"{chrom}\t{count}\n")
    f.write(f"\nTotal runtime: {hpc_time:.2f} seconds\n")

# Plot variant distribution
plt.figure(figsize=(10, 6))
sns.barplot(x=list(hpc_variant_counts.keys()), y=list(hpc_variant_counts.values()), palette="rocket")
plt.title("Variant Count per Chromosome (HPC)")
plt.xlabel("Chromosome")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig("results/plots/hpc_variant_distribution.png")
plt.close()
