import pandas as pd
import glob
from pathlib import Path

DATA_DIR = Path(r'C:\Users\richa\Documents\HPV sim Project\Code\ControlCode\NetworkCSVs')

node_files = glob.glob(str(DATA_DIR / "all_seeds_graph_nodes*.csv"))

dfs = []

for f in node_files:
    df = pd.read_csv(f)
    # Remove header rows
    df = df[df["seed"] != "seed"]
    dfs.append(df)

nodes = pd.concat(dfs, ignore_index=True)

# Convert seed to numeric properly
nodes["seed"] = pd.to_numeric(nodes["seed"], errors="coerce")
nodes = nodes.dropna(subset=["seed"])

# Remove duplicates
nodes = nodes.drop_duplicates(subset=["seed", "node"])

# Sort cleanly
nodes = nodes.sort_values(["seed", "node"]).reset_index(drop=True)
nodes.to_csv(DATA_DIR / "combined_nodes.csv", index=False)
