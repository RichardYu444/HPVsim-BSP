import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from pathlib import Path

edges_path = r"combined_edges.csv"
nodes_path = r"combined_nodes.csv"

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
print("First 10 seeds:", seeds[:10])

all_deg = []

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
    #Debugging
    edge_nodes = set(seed_edges["source"]).union(set(seed_edges["target"]))
    missing = edge_nodes - set(seed_nodes["node"])

    if missing:
        print("⚠ WARNING: Missing nodes:", len(missing))
    else:
        print("All edge nodes present.")

    #Degree stats
    degrees = np.array([d for _, d in G.degree()], dtype=int)
    all_deg.append(degrees)

    mean_deg = degrees.mean() if len(degrees) else float("nan")
    print(f"Mean degree (seed {seed}): {mean_deg:.4f}")

#Combine all degrees
all_deg = np.concatenate(all_deg)

print("\n===================================")
print("Mean degree across all seeds:", np.mean(all_deg))
print("Total nodes across all seeds:", len(all_deg))

#Cumulative Degree Distribution
unique_deg, counts = np.unique(all_deg, return_counts=True)
props = counts / counts.sum()
cum_prop = np.cumsum(props)

unique_deg, counts = np.unique(all_deg, return_counts=True)

# Remove zero degree (cannot plot log(0))
mask = unique_deg > 0
unique_deg = unique_deg[mask]
counts = counts[mask]

props = counts / counts.sum()
cum_prop = np.cumsum(props)

plt.figure()

plt.plot(unique_deg, cum_prop)

plt.xscale("log")   # 🔹 Log scale on x-axis
plt.ylim(0, 1)

plt.title("Cumulative Degree Distribution - Random Network")
plt.xlabel("Number of Partners (log scale)")
plt.ylabel("Cumulative Distribution")

plt.fill_between(unique_deg, 0, cum_prop, alpha=0.3)

plt.tight_layout()
plt.show()