"""
VNL 2024 Men — Data Loader & Preprocessing
Loads all 7 CSV files, cleans them, and merges into a master DataFrame.
"""

import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

FILE_MAP = {
    "players":   "VNL2024Men_Players.csv",
    "scorers":   "VNL2024Men_Scorers.csv",
    "attackers": "VNL2024Men_Attackers.csv",
    "blockers":  "VNL2024Men_Blockers.csv",
    "diggers":   "VNL2024Men_Diggers.csv",
    "receivers": "VNL2024Men_Receivers.csv",
    "servers":   "VNL2024Men_Servers.csv",
    "setters":   "VNL2024Men_Setters.csv",
}


def load_raw() -> dict[str, pd.DataFrame]:
    """Load all raw CSVs into a dict of DataFrames."""
    dfs = {}
    for key, fname in FILE_MAP.items():
        path = DATA_DIR / fname
        dfs[key] = pd.read_csv(path, encoding="latin1")
    return dfs


def build_master(dfs: dict[str, pd.DataFrame] | None = None) -> pd.DataFrame:
    """
    Merge all tables on (Name, Team) into a single master DataFrame.
    Fills missing numeric values with 0.
    """
    if dfs is None:
        dfs = load_raw()

    master = dfs["players"].copy()

    merges = [
        ("scorers",   ["Name", "Team"], None),
        ("attackers", ["Name", "Team"], ["Pt_Attack", "Err_Attack", "Att_Attack", "MAvg_Attack", "p_Attack"]),
        ("blockers",  ["Name", "Team"], ["Pt_Block", "Err_Block", "Rebounds", "MAvg_Block", "p_Block"]),
        ("diggers",   ["Name", "Team"], ["Sf_Dig", "Err_Dig", "MAvg_Dig", "p_Dig", "T_Dig"]),
        ("receivers", ["Name", "Team"], ["Sf_Receive", "Err_Receive", "Att_Receive", "MAvg_Receive", "p_Receive"]),
        ("servers",   ["Name", "Team"], ["Pt_Serve", "Err_Serve", "Att_Serve", "MAvg_Serve", "p_Serve"]),
        ("setters",   ["Name", "Team"], ["Sf_Set", "Err_Set", "Att_Set", "MAvg_Set", "p_Set", "Tot_Set"]),
    ]

    for table, keys, cols in merges:
        right = dfs[table][keys + cols] if cols else dfs[table]
        master = master.merge(right, on=keys, how="left")

    master = master.fillna(0)
    master["Age"] = 2024 - master["Birth_Year"]
    return master


def team_summary(master: pd.DataFrame) -> pd.DataFrame:
    """Aggregate team-level scoring totals."""
    agg = (
        master.groupby("Team")
        .agg(
            Total_Pts=("Tot_Pts", "sum"),
            Total_Atk=("Tot_Atk", "sum"),
            Total_Block=("Tot_Block", "sum"),
            Total_Serve=("Tot_Serve", "sum"),
            Players=("Name", "count"),
        )
        .reset_index()
        .sort_values("Total_Pts", ascending=False)
        .reset_index(drop=True)
    )
    agg["Rank"] = agg.index + 1
    return agg


if __name__ == "__main__":
    dfs = load_raw()
    master = build_master(dfs)
    print(f"Master shape: {master.shape}")
    print(f"Positions: {sorted(master['Position'].unique())}")
    print(f"Teams: {sorted(master['Team'].unique())}")
    print(master.head(3).to_string())
