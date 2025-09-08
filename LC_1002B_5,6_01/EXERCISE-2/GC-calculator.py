from Bio.Seq import Seq
from Bio.Data import CodonTable

# --- 1. Define a sample DNA sequence ---
dna_sequence = Seq(""">PL382336.1 KR 1020240170863-A/1: Microbiome engineering using Saccharomyces boulardii secreting human lysozyme
AAGGTTTTCGAACGTTGTGAATTGGCCAGAACTTTGAAGAGATTGGGTATGGACGGTTACCGTGGTATCT
CTTTGGCTAACTGGATGTGTTTGGCCAAGTGGGAATCTGGTTACAACACTAGAGCTACTAACTACAACGC
CGGTGACCGTTCTACTGACTACGGTATCTTCCAAATTAACTCTAGATACTGGTGTAACGACGGTAAGACT
CCAGGCGCCGTTAACGCCTGTCAGTTGTCTTGTTCTGCTTTGTTGCAAGACAACATCGCTGACGCCGTTG
CCTGTGCTAAGAGAGTCGTTAGAGACCCACAAGGTATCAGAGCTTGGGTCGCTTGGCGTAACAGATGTCA
AAACAGAGACGTCAGACAATACGTTCAAGGTTGTGGTGTC""")
print("Original DNA Sequence:")
print(dna_sequence)
print("-" * 50)

# Remove the header line from the sequence
dna_sequence = Seq("".join(str(dna_sequence).splitlines()[1:]))


# --- 2. Calculate GC Content ---
gc_content = (dna_sequence.count("G") + dna_sequence.count("C")) / len(dna_sequence) * 100
print(f"GC Content of the DNA sequence: {gc_content:.2f}%")
print("-" * 50)


# --- 3. Find a Motif in the DNA Sequence ---
# A motif is a short, recurring pattern in a sequence. Finding them is crucial for identifying functional regions like transcription factor binding sites.
motif_to_find = "ATGC"
print(f"Searching for the motif '{motif_to_find}'...")

# Use a list to store the starting positions of the motif
motif_positions = []
start_index = -1
while True:
    start_index = dna_sequence.find(motif_to_find, start_index + 1)
    if start_index == -1:
        break
    motif_positions.append(start_index)

if motif_positions:
    print(f"Motif found at the following zero-based positions: {motif_positions}")
else:
    print("Motif not found in the sequence.")
print("-" * 50)


# --- 4. Translate the Nucleotide Sequence into a Protein Sequence ---

protein_sequence = dna_sequence.translate(to_stop=True)
print("Translated Protein Sequence:")
print(protein_sequence)
print("-" * 50)

# we can also specify a different codon table if needed.
vertebrate_mito_table = CodonTable.unambiguous_dna_by_id[2]
protein_mito = dna_sequence.translate(table=vertebrate_mito_table, to_stop=True)
print("Translated Protein Sequence (Vertebrate Mitochondrial Table):")
print(protein_mito)
