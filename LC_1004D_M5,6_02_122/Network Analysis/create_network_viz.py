import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.patches import Circle
import seaborn as sns

# Load the data
edges_df = pd.read_csv('protein_network_data.tsv', sep='\t')
nodes_df = pd.read_csv('protein_nodes.tsv', sep='\t')

print("Network Data Summary:")
print(f"Number of edges: {len(edges_df)}")
print(f"Number of nodes: {len(nodes_df)}")
print(f"Average interaction score: {edges_df['score'].mean():.3f}")

# Create network graph
G = nx.from_pandas_edgelist(edges_df, source='node1', target='node2', edge_attr='score')

# Calculate network metrics
degree_centrality = nx.degree_centrality(G)
betweenness_centrality = nx.betweenness_centrality(G)
closeness_centrality = nx.closeness_centrality(G)
eigenvector_centrality = nx.eigenvector_centrality(G)

# Create centrality dataframe
centrality_df = pd.DataFrame({
    'protein_id': list(degree_centrality.keys()),
    'degree_centrality': list(degree_centrality.values()),
    'betweenness_centrality': list(betweenness_centrality.values()),
    'closeness_centrality': list(closeness_centrality.values()),
    'eigenvector_centrality': list(eigenvector_centrality.values())
})

# Merge with node attributes
final_nodes_df = nodes_df.merge(centrality_df, on='protein_id', how='left')

# Save enhanced datasets for Tableau
final_nodes_df.to_csv('enhanced_protein_nodes.csv', index=False)
edges_df.to_csv('protein_interactions.csv', index=False)

print("\nFiles created for Tableau:")
print("- enhanced_protein_nodes.csv")
print("- protein_interactions.csv")

# Create a basic network visualization
plt.figure(figsize=(12, 10))
pos = nx.spring_layout(G, k=2, iterations=50)

# Node sizes based on degree centrality
node_sizes = [degree_centrality[node] * 3000 for node in G.nodes()]

# Node colors based on protein type
protein_types = nodes_df.set_index('protein_id')['protein_type'].to_dict()
color_map = {'GPCR': 'red', 'Enzyme': 'green', 'Growth Factor': 'blue', 
             'G-protein': 'orange', 'Transporter': 'purple', 'Regulatory': 'brown'}
node_colors = [color_map.get(protein_types.get(node, 'Unknown'), 'gray') for node in G.nodes()]

# Draw network
nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color=node_colors, alpha=0.7)
nx.draw_networkx_labels(G, pos, font_size=8, font_weight='bold')

# Edge weights based on interaction scores
edge_weights = [edges_df[edges_df['node1'] == edge[0]]['score'].iloc[0] if len(edges_df[edges_df['node1'] == edge[0]]) > 0 
                else edges_df[edges_df['node2'] == edge[0]]['score'].iloc[0] for edge in G.edges()]
nx.draw_networkx_edges(G, pos, width=[w*3 for w in edge_weights], alpha=0.6, edge_color='gray')

plt.title('Dopamine-Related Protein-Protein Interaction Network', fontsize=16, fontweight='bold')
plt.axis('off')

# Create legend
legend_elements = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color, 
                             markersize=10, label=ptype) for ptype, color in color_map.items()]
plt.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(1.15, 1))

plt.tight_layout()
plt.savefig('network_preview.png', dpi=300, bbox_inches='tight')
plt.show()

print("\nNetwork preview saved as 'network_preview.png'")
