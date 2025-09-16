import pandas as pd
import numpy as np
import networkx as nx

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

print("\nTop 5 most central proteins by degree centrality:")
print(final_nodes_df.nlargest(5, 'degree_centrality')[['protein_id', 'protein_name', 'degree_centrality']])
