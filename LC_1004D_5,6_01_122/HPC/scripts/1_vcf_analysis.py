import os

# Create results folders
os.makedirs("results/plots", exist_ok=True)
os.makedirs("results/reports", exist_ok=True)

import cyvcf2
import time
import matplotlib.pyplot as plt
import seaborn as sns

# Start timer
start_time = time.time()

# Load VCF file
vcf_path = "Target.vcf"
vcf = cyvcf2.VCF(vcf_path)

# Count variants per chromosome
variant_counts = {}
for variant in vcf:
    chrom = variant.CHROM
    variant_counts[chrom] = variant_counts.get(chrom, 0) + 1

# End timer
standard_time = time.time() - start_time

# Save report
with open("results/reports/standard_variant_counts.txt", "w") as f:
    for chrom, count in variant_counts.items():
        f.write(f"{chrom}\t{count}\n")
    f.write(f"\nTotal runtime: {standard_time:.2f} seconds\n")

# Plot variant distribution
plt.figure(figsize=(10, 6))
sns.barplot(x=list(variant_counts.keys()), y=list(variant_counts.values()), palette="mako")
plt.title("Variant Count per Chromosome (Standard)")
plt.xlabel("Chromosome")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig("results/plots/standard_variant_distribution.png")
plt.close()