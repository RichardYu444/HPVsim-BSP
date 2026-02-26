import pandas as pd
import glob
from pathlib import Path

DATA_DIR = Path(r"C:\Users\richa\Documents\HPV sim Project\Code\ControlCode\NetworkCSVs")

edge_files = glob.glob(str(DATA_DIR / "all_seeds_graph_edges*.csv"))

dfs = []

for f in edge_files:
    df = pd.read_csv(f)

    # Remove accidental header rows written during append
    df = df[df["seed"] != "seed"]

    dfs.append(df)

edges = pd.concat(dfs, ignore_index=True)

edges["seed"] = pd.to_numeric(edges["seed"], errors="coerce")
#Remove rows where seed is missing
edges = edges.dropna(subset=["seed"])

#Drop duplicates
edges = edges.drop_duplicates(subset=["seed", "source", "target"])

#Sort cleanly
edges = edges.sort_values(["seed", "source", "target"]).reset_index(drop=True)

# ---- Save clean file ----
edges.to_csv(DATA_DIR / "combined_edges.csv", index=False)

print("Final shape:", edges.shape)
print("Missing seed rows:", edges["seed"].isna().sum())
print("Seed dtype:", edges["seed"].dtype)