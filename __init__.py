"""
VNL 2024 Men — Player Rankings & Composite Scores

Scoring methodology
-------------------
Best Attacker  : weighted by Pt_Attack (50%) + p_Attack (30%) + MAvg_Attack (20%)
Best Libero    : weighted by Sf_Dig (40%) + p_Dig (30%) + Sf_Receive (40%) + p_Receive (30%)
                 (weights normalised so total = 1 after division)
Best MB        : weighted by Pt_Block (50%) + Pt_Attack (30%) + p_Attack (20%)
Best Server    : ace points (Pt_Serve) — secondary sort by p_Serve %
"""

import pandas as pd
from src.data_loader import build_master


# ---------------------------------------------------------------------------
# Composite score helpers
# ---------------------------------------------------------------------------

def score_attackers(df: pd.DataFrame) -> pd.DataFrame:
    """All positions, sorted by attack score."""
    d = df[df["Pt_Attack"] > 0].copy()
    # Normalise each component to 0-1 within the pool, then weight
    d["_atk_n"] = d["Pt_Attack"]   / d["Pt_Attack"].max()
    d["_eff_n"] = d["p_Attack"]    / d["p_Attack"].max()
    d["_avg_n"] = d["MAvg_Attack"] / d["MAvg_Attack"].max()
    d["attack_score"] = (d["_atk_n"] * 0.50 + d["_eff_n"] * 0.30 + d["_avg_n"] * 0.20) * 100
    cols = ["Name", "Team", "Position", "Height", "Age",
            "Pt_Attack", "Err_Attack", "Att_Attack", "p_Attack", "MAvg_Attack", "attack_score"]
    return (
        d[cols]
        .sort_values("attack_score", ascending=False)
        .round(2)
        .reset_index(drop=True)
    )


def score_liberos(df: pd.DataFrame) -> pd.DataFrame:
    """Liberos only (Position == 'L')."""
    d = df[df["Position"] == "L"].copy()
    # Raw composite (not normalised — keeps intuitive scale)
    d["libero_score"] = (
        d["Sf_Dig"]    * 0.40 +
        d["p_Dig"]     * 0.30 +
        d["Sf_Receive"]* 0.40 +
        d["p_Receive"] * 0.30
    )
    cols = ["Name", "Team", "Height", "Age",
            "Sf_Dig", "Err_Dig", "p_Dig",
            "Sf_Receive", "Err_Receive", "p_Receive",
            "libero_score"]
    return (
        d[cols]
        .sort_values("libero_score", ascending=False)
        .round(2)
        .reset_index(drop=True)
    )


def score_middle_blockers(df: pd.DataFrame) -> pd.DataFrame:
    """Middle Blockers only (Position == 'MB')."""
    d = df[df["Position"] == "MB"].copy()
    d["mb_score"] = (
        d["Pt_Block"]  * 0.50 +
        d["Pt_Attack"] * 0.30 +
        d["p_Attack"]  * 0.20
    )
    cols = ["Name", "Team", "Height", "Age",
            "Pt_Block", "Err_Block", "p_Block",
            "Pt_Attack", "p_Attack",
            "mb_score"]
    return (
        d[cols]
        .sort_values("mb_score", ascending=False)
        .round(2)
        .reset_index(drop=True)
    )


def score_setters(df: pd.DataFrame) -> pd.DataFrame:
    """Setters only (Position == 'S') — judged on volume, efficiency, consistency."""
    d = df[df["Position"] == "S"].copy()
    d = d[d["Sf_Set"] > 0]
    d["_vol_n"] = d["Sf_Set"]    / d["Sf_Set"].max()
    d["_eff_n"] = d["p_Set"]     / d["p_Set"].max()
    d["_avg_n"] = d["MAvg_Set"]  / d["MAvg_Set"].max()
    d["setter_score"] = (d["_vol_n"] * 0.50 + d["_eff_n"] * 0.30 + d["_avg_n"] * 0.20) * 100
    cols = ["Name", "Team", "Height", "Age",
            "Sf_Set", "Err_Set", "Att_Set", "p_Set", "MAvg_Set", "setter_score"]
    return (
        d[cols]
        .sort_values("setter_score", ascending=False)
        .round(2)
        .reset_index(drop=True)
    )


def score_servers(df: pd.DataFrame) -> pd.DataFrame:
    """All positions, sorted by ace points then efficiency."""
    d = df[df["Pt_Serve"] > 0].copy()
    cols = ["Name", "Team", "Position",
            "Pt_Serve", "Err_Serve", "Att_Serve", "p_Serve", "MAvg_Serve"]
    return (
        d[cols]
        .sort_values(["Pt_Serve", "p_Serve"], ascending=False)
        .round(2)
        .reset_index(drop=True)
    )


def top_scorers(df: pd.DataFrame, n: int = 20) -> pd.DataFrame:
    """Overall point scorers across all phases."""
    cols = ["Name", "Team", "Position", "Height", "Age",
            "Tot_Pts", "Tot_Atk", "Tot_Block", "Tot_Serve"]
    return (
        df[cols]
        .sort_values("Tot_Pts", ascending=False)
        .head(n)
        .round(1)
        .reset_index(drop=True)
    )


# ---------------------------------------------------------------------------
# Convenience: run all rankings at once
# ---------------------------------------------------------------------------

def all_rankings(master: pd.DataFrame | None = None) -> dict[str, pd.DataFrame]:
    if master is None:
        master = build_master()
    return {
        "attackers":      score_attackers(master),
        "liberos":        score_liberos(master),
        "middle_blockers":score_middle_blockers(master),
        "setters":        score_setters(master),
        "servers":        score_servers(master),
        "top_scorers":    top_scorers(master),
    }


if __name__ == "__main__":
    master = build_master()
    ranks  = all_rankings(master)

    for name, df in ranks.items():
        print(f"\n{'='*60}")
        print(f"  {name.upper()}")
        print(f"{'='*60}")
        print(df.head(10).to_string(index=False))
