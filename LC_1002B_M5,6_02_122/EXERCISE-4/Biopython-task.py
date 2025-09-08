from Bio import Entrez, SeqIO
from Bio.SeqUtils import gc_fraction
import matplotlib.pyplot as plt

# Step 1: Fetch a sequence from NCBI
Entrez.email = "email"   # Always provide an email to NCBI
accession_id = "NM_001200025"  # Example: BRCA1 gene transcript

handle = Entrez.efetch(db="nucleotide", id=accession_id, rettype="fasta", retmode="text")
record = SeqIO.read(handle, "fasta")
handle.close()

print(f"Sequence ID: {record.id}")
print(f"Description: {record.description}")
print(f"Sequence length: {len(record.seq)}")

# Step 2: Sequence Analysis
gc_content = gc_fraction(record.seq) * 100
print(f"GC Content: {gc_content:.2f}%")

# Step 3: Visualization - Nucleotide composition
nucleotides = ["A", "T", "G", "C"]
counts = [record.seq.count(base) for base in nucleotides]

plt.bar(nucleotides, counts, color=["skyblue", "lightgreen", "salmon", "orange"])
plt.title(f"Nucleotide composition of {accession_id}")
plt.xlabel("Nucleotide")
plt.ylabel("Count")
plt.show()
