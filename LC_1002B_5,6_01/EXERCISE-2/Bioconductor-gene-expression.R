# Step 1: Install and load Bioconductor packages
if (!requireNamespace("BiocManager", quietly = TRUE))
    install.packages("BiocManager")

BiocManager::install(c("DESeq2", "airway", "apeglm", "EnhancedVolcano"))

library(DESeq2)
library(airway)            # Example dataset
library(EnhancedVolcano)   # For visualization

# Step 2: Load example RNA-seq dataset
data("airway")
se <- airway
# airway dataset: RNA-seq counts from airway smooth muscle cells treated with dexamethasone

# Step 3: Prepare data for DESeq2
dds <- DESeqDataSet(se, design = ~ cell + dex)  # 'dex' is treatment factor
dds <- dds[rowSums(counts(dds)) > 1, ]          # Filter out low-count genes

# Step 4: Run differential expression analysis
dds <- DESeq(dds)
res <- results(dds, contrast = c("dex", "trt", "untrt"))  # treated vs untreated

# Step 5: View summary of results
summary(res)

# Step 6: Visualization
# MA Plot
plotMA(res, ylim=c(-5,5))

# Volcano Plot
EnhancedVolcano(res,
    lab = rownames(res),
    x = 'log2FoldChange',
    y = 'pvalue',
    title = 'Differential Expression (Treated vs Untreated)',
    pCutoff = 0.05,
    FCcutoff = 1.0
)
