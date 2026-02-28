import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from pathlib import Path

#uses same set up as degree.py but has the clustering function instead to calculate clustering coeffcients

edges_path = r"combined_edges.csv"
nodes_path = r"combined_nodes.csv"

def four_cycle_clustering(G):
    clustering = {}
    for node in G.nodes():
        neighbors = set(G.neighbors(node))
        k = len(neighbors)
        
        if k < 2:
            clustering[node] = 0
            continue
        # Possible neighbor pairs
        possible = k * (k - 1) / 2
        
        square_count = 0
        
        neighbors_list = list(neighbors)
        
        for i in range(len(neighbors_list)):
            for j in range(i + 1, len(neighbors_list)):
                u = neighbors_list[i]
                v = neighbors_list[j]
                
                # Nodes connected to both u and v
                common = set(G.neighbors(u)) & set(G.neighbors(v))
                
                # Remove self if present
                common.discard(node)
                
                square_count += len(common)
        
        clustering[node] = square_count / possible if possible > 0 else 0.0
    
    return clustering

print("Loading CSVs...")
edges_df = pd.read_csv(edges_path)
nodes_df = pd.read_csv(nodes_path)

print("Edges shape:", edges_df.shape)
print("Nodes shape:", nodes_df.shape)

#Ensure seed numeric
edges_df["seed"] = pd.to_numeric(edges_df["seed"], errors="coerce")
nodes_df["seed"] = pd.to_numeric(nodes_df["seed"], errors="coerce")

#Drop bad rows
edges_df = edges_df.dropna(subset=["seed"])
nodes_df = nodes_df.dropna(subset=["seed"])

edges_df["seed"] = edges_df["seed"].astype(int)
nodes_df["seed"] = nodes_df["seed"].astype(int)

seeds = sorted(nodes_df["seed"].unique())

print(f"Found {len(seeds)} unique seeds")

for seed in seeds:
    print("\n==============================")
    print(f"Processing seed {seed}")
    seed_nodes = nodes_df[nodes_df["seed"] == seed]
    seed_edges = edges_df[edges_df["seed"] == seed]
    print("Seed nodes:", len(seed_nodes))
    print("Seed edges:", len(seed_edges))
    #Build graph
    G = nx.Graph()

    #Add nodes
    for _, row in seed_nodes.iterrows():
        if "bipartite" in seed_nodes.columns:
            G.add_node(row["node"], bipartite=row.get("bipartite"))
        else:
            G.add_node(row["node"])

    #Add edges
    G.add_edges_from(
        zip(seed_edges["source"], seed_edges["target"])
    )
    clustering = four_cycle_clustering(G)