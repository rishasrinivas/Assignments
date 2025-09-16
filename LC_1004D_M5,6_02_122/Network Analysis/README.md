# Bioinformatics Network Visualization Project

## Overview
This project demonstrates advanced network visualization techniques for bioinformatics data, specifically focusing on protein-protein interaction networks related to dopamine signaling pathways.

## Dataset
- **Source**: STRING Database (https://string-db.org/)
- **Focus**: Dopamine-related proteins (DRD4 and interacting partners)
- **Network Size**: 11 proteins, 22 interactions
- **Average Interaction Score**: 0.812

## Key Proteins in the Network
1. **DRD4** (Dopamine Receptor D4) - Most central protein (degree centrality: 0.8)
2. **DRD2** (Dopamine Receptor D2) - High centrality (degree centrality: 0.6)
3. **COMT** (Catechol O-methyltransferase) - Key enzyme (degree centrality: 0.5)
4. **BDNF** (Brain-derived neurotrophic factor) - Growth factor (degree centrality: 0.4)

## Visualization Features

### Advanced Network Analysis
- **Centrality Metrics**: Degree, betweenness, closeness, and eigenvector centrality
- **Node Sizing**: Dynamic sizing based on centrality measures or molecular weight
- **Edge Weighting**: Link thickness represents interaction confidence scores
- **Color Coding**: Proteins grouped by functional type (GPCR, Enzyme, etc.)

### Interactive Features
1. **Filtering**: Filter nodes by protein type
2. **Threshold Control**: Adjust interaction strength threshold
3. **Dynamic Sizing**: Change node size metric in real-time
4. **Tooltips**: Detailed protein information on hover
5. **Drag & Drop**: Interactive node positioning

### Protein Categories
- **GPCR** (Red): G-protein coupled receptors (DRD2, DRD3, DRD4)
- **Enzyme** (Teal): Metabolic enzymes (COMT, MAOA)
- **Growth Factor** (Blue): Signaling molecules (BDNF)
- **G-protein** (Yellow): Signal transduction (GNAI1, GNB3)
- **Transporter** (Purple): Membrane transporters (SLC6A3, SLC6A4)
- **Regulatory** (Brown): Regulatory proteins (KLHL12)

## Files Generated

### Data Files
- `protein_network_data.tsv`: Raw interaction data
- `protein_nodes.tsv`: Node attributes
- `enhanced_protein_nodes.csv`: Nodes with centrality metrics
- `protein_interactions.csv`: Edge list for Tableau

### Visualization Files
- `network_visualization.html`: Interactive D3.js visualization
- `network_visualization.twb`: Tableau workbook template
- `simple_network_prep.py`: Python analysis script

## Technical Implementation

### Technologies Used
- **D3.js v7**: Interactive network visualization
- **Python**: NetworkX for graph analysis
- **HTML5/CSS3**: Modern web interface
- **Tableau**: Business intelligence visualization

### Network Analysis Metrics
- **Degree Centrality**: Number of direct connections
- **Betweenness Centrality**: Importance as network bridge
- **Closeness Centrality**: Average distance to all nodes
- **Eigenvector Centrality**: Influence based on connected nodes

## Biological Insights

### Key Findings
1. **DRD4 is the most central protein** - highest degree and eigenvector centrality
2. **Strong receptor family clustering** - DRD2, DRD3, DRD4 form tight cluster
3. **COMT bridges metabolic and signaling** - connects enzymes to receptors
4. **G-protein coupling is critical** - GNAI1 connects multiple receptors

### Pathway Analysis
- **Dopamine Signaling**: Central theme with DRD2/3/4 receptors
- **Neurotransmitter Metabolism**: COMT and MAOA regulate dopamine
- **Transport Systems**: SLC6A3/4 control neurotransmitter reuptake
- **Signal Transduction**: G-proteins mediate receptor signaling

## Usage Instructions

### Web Visualization
1. Open `network_visualization.html` in a web browser
2. Use controls to filter and explore the network
3. Hover over nodes for detailed information
4. Drag nodes to rearrange the layout

### Tableau Analysis
1. Open Tableau Desktop
2. Import `enhanced_protein_nodes.csv` and `protein_interactions.csv`
3. Use the provided `.twb` template as starting point
4. Create custom dashboards with network metrics

### Python Analysis
```bash
python3 simple_network_prep.py
```

## Future Enhancements
- Integration with additional databases (KEGG, Reactome)
- Time-series analysis of expression data
- 3D network visualization
- Machine learning for pathway prediction
- Integration with genomic variant data

## References
- STRING Database: https://string-db.org/
- NetworkX Documentation: https://networkx.org/
- D3.js Network Examples: https://observablehq.com/@d3/force-directed-graph
- Tableau Network Visualization Guide
