import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from pathlib import Path

edges_path = r"all_seeds_graph_edges.csv"
nodes_path = r"all_seeds_graph_nodes.csv"
all_deg = []
#as each run is appended into the same csv file, we first want to split them into each run
def split_runs(raw_df, header_vals):
    """Split a raw CSV (read with header=None) into runs separated by repeated header rows."""
    col1, col2 = header_vals
    header_mask = (raw_df.iloc[:, 1] == col1) & (raw_df.iloc[:, 2] == col2)
    header_idxs = list(raw_df.index[header_mask])
    if not header_idxs:
        raise ValueError(f"No repeated headers found matching {header_vals}")

    runs = []
    for j, start_idx in enumerate(header_idxs):
        end_idx = header_idxs[j + 1] if j + 1 < len(header_idxs) else len(raw_df)
        chunk = raw_df.iloc[start_idx + 1:end_idx].copy()
        # drop empty rows
        chunk = chunk[(chunk.iloc[:, 1] != "") & (chunk.iloc[:, 2] != "")]
        runs.append(chunk.reset_index(drop=True))
    return runs

# Read raw (because you have repeated headers + saved index column)
edges_raw = pd.read_csv(edges_path, header=None, dtype=str, keep_default_na=False)
nodes_raw = pd.read_csv(nodes_path, header=None, dtype=str, keep_default_na=False)

edge_runs = split_runs(edges_raw, ("source", "target"))
node_runs = split_runs(nodes_raw, ("node", "bipartite"))

out_dir = Path("degree_plots")
out_dir.mkdir(exist_ok=True)

n_runs = min(len(edge_runs), len(node_runs))
print(f"Found {len(edge_runs)} edge runs and {len(node_runs)} node runs. Using {n_runs} paired runs.")

for run_i in range(n_runs):
    eraw = edge_runs[run_i]
    nraw = node_runs[run_i]

    # Build edges df (col 0 is the old CSV index; col 1/2 are the actual fields)
    edges_df = pd.DataFrame({
        "source": eraw.iloc[:, 1].astype(str).values,
        "target": eraw.iloc[:, 2].astype(str).values,
    })

    # Build nodes df
    nodes_df = pd.DataFrame({
        "node": nraw.iloc[:, 1].astype(str).values,
        "bipartite": pd.to_numeric(nraw.iloc[:, 2], errors="coerce"),
    })

    # Rebuild graph (include all nodes so isolates are counted too)
    G = nx.Graph()
    for _, row in nodes_df.iterrows():
        if pd.notna(row["bipartite"]):
            G.add_node(row["node"], bipartite=int(row["bipartite"]))
        else:
            G.add_node(row["node"])
    G.add_edges_from(edges_df.itertuples(index=False, name=None))

    # Degree stats
    degrees = np.array([d for _, d in G.degree()], dtype=int)
    all_deg.append(degrees)
    mean_deg = degrees.mean() if len(degrees) else float("nan")
    print(f"Run {run_i+1}: nodes={G.number_of_nodes()} edges={G.number_of_edges()} mean_degree={mean_deg:.4f}")

    #unique_deg, counts = np.unique(degrees, return_counts=True)

    #props = counts / G.number_of_nodes()  # proportions (sums to 1)

    #plt.figure(figsize=(6, 4))
    #plt.bar(unique_deg, props, width=0.9)

    #plt.xlabel("Degree")
    #plt.ylabel("Proportion of nodes")
    #plt.title(f"Degree distribution (run {run_i+1})")

    # x-axis: integers only
    #from matplotlib.ticker import MaxNLocator
    #ax = plt.gca()
    #ax.xaxis.set_major_locator(MaxNLocator(integer=True))

    #plt.tight_layout()


    #plot_path = out_dir / f"degree_distribution_run_{run_i+1}.png"
    #plt.savefig(plot_path, dpi=200)
    #plt.close()

all_deg = np.concat(all_deg)
print("Mean degree across all runs, all nodes: ", np.average(all_deg))
unique_deg, counts = np.unique(degrees, return_counts=True)
np.append(0, unique_deg)
props = counts / sum(counts)
cum_prop = [0]
dummy = 0
for prop in props:
    dummy += prop
    cum_prop.append(dummy)
fig, ax = plt.subplots()
ax.plot(np.arange(0, 14), cum_prop)
plt.ylim(bottom = 0, top = 1)
plt.title('Cumulative Degree Distribution- Random Network')
plt.xlabel('Number of Partners')
plt.ylabel('Cumulative Distribution')
plt.xlim(left = 0, right = 13)
ax.fill_between(np.arange(0, 14), 0, cum_prop, color = 'lightsteelblue')
plt.show()