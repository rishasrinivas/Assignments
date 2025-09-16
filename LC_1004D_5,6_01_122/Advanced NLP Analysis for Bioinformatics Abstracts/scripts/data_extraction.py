#step1: Instaltion
!pip install Biopython

# Step 2: Import required libraries
from Bio import Entrez
import time

# Step 3: Set your email (required by NCBI)
Entrez.email = "121321050026@sfc.ac.in"  # Replace with your email


# Step 4: Search PubMed for colorectal cancer articles
search_term = "colorectal cancer"
handle = Entrez.esearch(db="pubmed", term=search_term, retmax=200)
record = Entrez.read(handle)
handle.close()
id_list = record["IdList"]

# Step 5: Fetch abstracts for the retrieved IDs
abstracts = []
for pmid in id_list:
    try:
        fetch_handle = Entrez.efetch(db="pubmed", id=pmid, rettype="abstract", retmode="text")
        abstract_text = fetch_handle.read()
        fetch_handle.close()
        abstracts.append(abstract_text)
        time.sleep(0.5)  
    except:
        continue

# Step 6: Save abstracts to a .txt file
with open("colorectal_cancer_abstracts.txt", "w", encoding="utf-8") as f:
    for abstract in abstracts:
        f.write(abstract.strip() + "\n\n---\n\n")

print(f"Saved {len(abstracts)} abstracts to colorectal_cancer_abstracts.txt")
