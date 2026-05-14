"""
VNL 2024 Men — Analysis & Insights
Team synergy, phase contribution, and player consistency notes.
"""

import pandas as pd
import numpy as np
from data_loader import build_master, team_summary


# ---------------------------------------------------------------------------
# Team synergy: how balanced is each team across Attack / Block / Serve?
# ---------------------------------------------------------------------------

def team_synergy(team_df: pd.DataFrame) -> pd.DataFrame:
    """
    Balance score: how evenly distributed are a team's points across the 3 phases?
    A perfectly balanced team scores 1/3 of its points from each phase.
    Uses 1 - normalised std-dev of the three phase shares.
    Higher = more balanced.
    """
    d = team_df.copy()
    d["atk_share"]   = d["Total_Atk"]   / d["Total_Pts"]
    d["block_share"] = d["Total_Block"]  / d["Total_Pts"]
    d["serve_share"] = d["Total_Serve"]  / d["Total_Pts"]

    shares = d[["atk_share", "block_share", "serve_share"]].values
    d["balance_score"] = (1 - shares.std(axis=1)) * 100  # 0-100

    d["dominant_phase"] = (
        d[["Total_Atk", "Total_Block", "Total_Serve"]]
        .idxmax(axis=1)
        .str.replace("Total_", "")
    )

    return d[["Team","Total_Pts","atk_share","block_share","serve_share",
              "balance_score","dominant_phase"]].sort_values("balance_score", ascending=False).round(3)


# ---------------------------------------------------------------------------
# Player phase contribution: what % of their team's score does each player account for?
# ---------------------------------------------------------------------------

def player_contribution(master: pd.DataFrame, team_df: pd.DataFrame) -> pd.DataFrame:
    d = master.merge(team_df[["Team", "Total_Pts"]], on="Team")
    d["contribution_pct"] = (d["Tot_Pts"] / d["Total_Pts"] * 100).round(2)
    cols = ["Name", "Team", "Position", "Tot_Pts", "Total_Pts", "contribution_pct"]
    return d[cols].sort_values("contribution_pct", ascending=False).reset_index(drop=True)


# ---------------------------------------------------------------------------
# Attack efficiency vs errors — risk profile
# ---------------------------------------------------------------------------

def attack_risk_profile(master: pd.DataFrame) -> pd.DataFrame:
    d = master[master["Att_Attack"] > 30].copy()
    d["kill_rate"]  = (d["Pt_Attack"]  / d["Att_Attack"] * 100).round(2)
    d["error_rate"] = (d["Err_Attack"] / d["Att_Attack"] * 100).round(2)
    d["style"] = pd.cut(
        d["error_rate"],
        bins=[0, 12, 18, 100],
        labels=["Conservative", "Balanced", "Aggressive"]
    )
    cols = ["Name","Team","Position","Att_Attack","kill_rate","error_rate","style"]
    return d[cols].sort_values("kill_rate", ascending=False).reset_index(drop=True)


# ---------------------------------------------------------------------------
# Age analysis
# ---------------------------------------------------------------------------

def age_analysis(master: pd.DataFrame) -> dict:
    return {
        "youngest_scorer":  master.nsmallest(1, "Birth_Year")[["Name","Team","Position","Age","Tot_Pts"]],
        "oldest_scorer":    master.nlargest(1, "Birth_Year")[["Name","Team","Position","Age","Tot_Pts"]],
        "avg_age_by_pos":   master.groupby("Position")["Age"].mean().round(1).sort_values(),
        "avg_age_by_team":  master.groupby("Team")["Age"].mean().round(1).sort_values(),
    }


# ---------------------------------------------------------------------------
# Height analysis
# ---------------------------------------------------------------------------

def height_analysis(master: pd.DataFrame) -> pd.DataFrame:
    return (
        master.groupby("Position")
        .agg(avg_height=("Height","mean"), max_height=("Height","max"), min_height=("Height","min"), n=("Name","count"))
        .round(1)
        .reset_index()
    )


# ---------------------------------------------------------------------------
# Print summary report
# ---------------------------------------------------------------------------

def print_report():
    master  = build_master()
    team_df = team_summary(master)

    print("=" * 65)
    print("  VNL 2024 MEN — ANALYSIS REPORT")
    print("=" * 65)

    print("\n📊 TEAM SYNERGY (balance across attack / block / serve)")
    print(team_synergy(team_df).head(8).to_string(index=False))

    print("\n👤 TOP INDIVIDUAL CONTRIBUTORS (% of team score)")
    print(player_contribution(master, team_df).head(10).to_string(index=False))

    print("\n⚡ ATTACK RISK PROFILES")
    rp = attack_risk_profile(master)
    for style in ["Aggressive", "Balanced", "Conservative"]:
        sub = rp[rp["style"] == style]
        print(f"  {style}: {len(sub)} players — avg kill {sub['kill_rate'].mean():.1f}%")

    age = age_analysis(master)
    print("\n📅 AVERAGE AGE BY POSITION")
    print(age["avg_age_by_pos"].to_string())

    print("\n📏 HEIGHT BY POSITION")
    print(height_analysis(master).to_string(index=False))


if __name__ == "__main__":
    print_report()
