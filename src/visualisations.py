"""
VNL 2024 Men — Visualisations
Generates and saves all charts to outputs/figures/.
"""

import matplotlib
matplotlib.use("Agg")  # headless — no display needed
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd
from pathlib import Path

OUT_DIR = Path(__file__).resolve().parent.parent / "outputs" / "figures"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# Style
# ---------------------------------------------------------------------------
PALETTE = {
    "blue":   "#2B6CB0",
    "green":  "#276749",
    "orange": "#C05621",
    "purple": "#553C9A",
    "red":    "#9B2C2C",
    "gray":   "#4A5568",
}
TEAM_COLORS = {
    "FRA":"#002395","SLO":"#003DA5","JPN":"#BC002D","POL":"#DC143C",
    "BRA":"#009C3B","CAN":"#FF0000","ARG":"#74ACDF","CUB":"#002A8F",
    "ITA":"#009246","NED":"#FF6600","SRB":"#C6363C","IRI":"#239F40",
    "GER":"#000000","TUR":"#E30A17","USA":"#3C3B6E","BUL":"#00966E",
}

def _save(fig, name: str):
    path = OUT_DIR / f"{name}.png"
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  Saved → {path}")


def _style_ax(ax, title="", xlabel="", ylabel=""):
    ax.set_title(title, fontsize=13, fontweight="bold", pad=12)
    ax.set_xlabel(xlabel, fontsize=10)
    ax.set_ylabel(ylabel, fontsize=10)
    ax.spines[["top", "right"]].set_visible(False)
    ax.tick_params(labelsize=9)
    ax.grid(axis="y", alpha=0.3, linestyle="--")


# ---------------------------------------------------------------------------
# 1. Team Total Points — horizontal bar
# ---------------------------------------------------------------------------
def plot_team_ranking(team_df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(10, 6))
    teams = team_df.sort_values("Total_Pts")
    colors = [TEAM_COLORS.get(t, PALETTE["gray"]) for t in teams["Team"]]
    bars = ax.barh(teams["Team"], teams["Total_Pts"], color=colors, edgecolor="white", linewidth=0.5)
    for bar, val in zip(bars, teams["Total_Pts"]):
        ax.text(bar.get_width() + 8, bar.get_y() + bar.get_height()/2,
                f"{int(val)}", va="center", fontsize=9)
    ax.set_xlim(0, teams["Total_Pts"].max() * 1.12)
    _style_ax(ax, title="VNL 2024 Men — Team Total Points", xlabel="Points")
    ax.grid(axis="x", alpha=0.3, linestyle="--")
    ax.grid(axis="y", alpha=0)
    fig.tight_layout()
    _save(fig, "01_team_ranking")


# ---------------------------------------------------------------------------
# 2. Team breakdown — stacked bar (Attack / Block / Serve)
# ---------------------------------------------------------------------------
def plot_team_breakdown(team_df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(12, 5))
    x = np.arange(len(team_df))
    w = 0.6
    b1 = ax.bar(x, team_df["Total_Atk"],   w, label="Attack", color=PALETTE["blue"])
    b2 = ax.bar(x, team_df["Total_Block"],  w, bottom=team_df["Total_Atk"],
                label="Block", color=PALETTE["green"])
    b3 = ax.bar(x, team_df["Total_Serve"],  w,
                bottom=team_df["Total_Atk"] + team_df["Total_Block"],
                label="Serve", color=PALETTE["orange"])
    ax.set_xticks(x)
    ax.set_xticklabels(team_df["Team"], rotation=45, ha="right")
    ax.legend(loc="upper right", fontsize=9)
    _style_ax(ax, title="VNL 2024 Men — Team Points Breakdown", ylabel="Points")
    fig.tight_layout()
    _save(fig, "02_team_breakdown")


# ---------------------------------------------------------------------------
# 3. Top 10 attackers — lollipop
# ---------------------------------------------------------------------------
def plot_top_attackers(atk_df: pd.DataFrame, n: int = 10):
    d = atk_df.head(n).sort_values("attack_score")
    fig, ax = plt.subplots(figsize=(9, 6))
    ax.hlines(range(len(d)), 0, d["attack_score"], color=PALETTE["orange"], linewidth=1.5, alpha=0.7)
    ax.scatter(d["attack_score"], range(len(d)), color=PALETTE["orange"], s=80, zorder=3)
    ax.set_yticks(range(len(d)))
    ax.set_yticklabels([f"{r['Name']} ({r['Team']})" for _, r in d.iterrows()], fontsize=10)
    for i, (_, r) in enumerate(d.iterrows()):
        ax.text(r["attack_score"] + 0.3, i, f"{r['attack_score']:.1f}", va="center", fontsize=8)
    _style_ax(ax, title="Top 10 Attackers — Composite Score\n(50% pts · 30% efficiency · 20% avg/match)",
              xlabel="Score (0–100)")
    ax.grid(axis="x", alpha=0.3, linestyle="--")
    ax.grid(axis="y", alpha=0)
    fig.tight_layout()
    _save(fig, "03_top_attackers")


# ---------------------------------------------------------------------------
# 4. Attack volume vs efficiency scatter
# ---------------------------------------------------------------------------
def plot_attack_scatter(atk_df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(9, 6))
    sc = ax.scatter(atk_df["Pt_Attack"], atk_df["p_Attack"],
                    c=[PALETTE["blue"] if p == "O" else PALETTE["orange"] if p == "OH" else PALETTE["purple"]
                       for p in atk_df["Position"]],
                    s=60, alpha=0.7, edgecolors="white", linewidths=0.5)
    # Label top 10
    for _, r in atk_df.head(10).iterrows():
        ax.annotate(r["Name"], (r["Pt_Attack"], r["p_Attack"]),
                    textcoords="offset points", xytext=(4, 3), fontsize=7)
    handles = [
        mpatches.Patch(color=PALETTE["blue"],   label="Opposite (O)"),
        mpatches.Patch(color=PALETTE["orange"], label="Outside Hitter (OH)"),
        mpatches.Patch(color=PALETTE["purple"], label="Other"),
    ]
    ax.legend(handles=handles, fontsize=8)
    _style_ax(ax, title="Attack Volume vs Efficiency", xlabel="Attack Points", ylabel="Efficiency %")
    fig.tight_layout()
    _save(fig, "04_attack_scatter")


# ---------------------------------------------------------------------------
# 5. Libero defence radar / bar comparison
# ---------------------------------------------------------------------------
def plot_libero_ranking(lib_df: pd.DataFrame, n: int = 10):
    d = lib_df.head(n).sort_values("libero_score")
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))

    # Left: combined score lollipop
    ax = axes[0]
    ax.hlines(range(len(d)), 0, d["libero_score"], color=PALETTE["green"], linewidth=1.5, alpha=0.7)
    ax.scatter(d["libero_score"], range(len(d)), color=PALETTE["green"], s=80, zorder=3)
    ax.set_yticks(range(len(d)))
    ax.set_yticklabels([f"{r['Name']} ({r['Team']})" for _, r in d.iterrows()], fontsize=10)
    _style_ax(ax, title="Libero Combined Defence Score", xlabel="Score")
    ax.grid(axis="x", alpha=0.3, linestyle="--")
    ax.grid(axis="y", alpha=0)

    # Right: digs vs receives grouped bar
    ax2 = axes[1]
    x  = np.arange(len(d))
    w  = 0.35
    ax2.barh(x - w/2, d["Sf_Dig"],     w, label="Successful Digs",     color=PALETTE["blue"],  alpha=0.85)
    ax2.barh(x + w/2, d["Sf_Receive"], w, label="Successful Receives",  color=PALETTE["purple"], alpha=0.85)
    ax2.set_yticks(x)
    ax2.set_yticklabels([f"{r['Name']}" for _, r in d.iterrows()], fontsize=10)
    ax2.legend(fontsize=9)
    _style_ax(ax2, title="Digs vs Receives (top 10 liberos)")
    ax2.grid(axis="x", alpha=0.3, linestyle="--")
    ax2.grid(axis="y", alpha=0)

    fig.suptitle("VNL 2024 Men — Best Liberos", fontsize=14, fontweight="bold", y=1.02)
    fig.tight_layout()
    _save(fig, "05_libero_ranking")


# ---------------------------------------------------------------------------
# 6. Middle Blocker ranking
# ---------------------------------------------------------------------------
def plot_mb_ranking(mb_df: pd.DataFrame, n: int = 10):
    d = mb_df.head(n).sort_values("mb_score")
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))

    ax = axes[0]
    ax.hlines(range(len(d)), 0, d["mb_score"], color=PALETTE["purple"], linewidth=1.5, alpha=0.7)
    ax.scatter(d["mb_score"], range(len(d)), color=PALETTE["purple"], s=80, zorder=3)
    ax.set_yticks(range(len(d)))
    ax.set_yticklabels([f"{r['Name']} ({r['Team']})" for _, r in d.iterrows()], fontsize=10)
    _style_ax(ax, title="MB Combined Score\n(50% blocks · 30% atk pts · 20% atk %)", xlabel="Score")
    ax.grid(axis="x", alpha=0.3, linestyle="--")
    ax.grid(axis="y", alpha=0)

    ax2 = axes[1]
    x = np.arange(len(d))
    w = 0.35
    ax2.barh(x - w/2, d["Pt_Block"],  w, label="Block Points",  color=PALETTE["purple"], alpha=0.85)
    ax2.barh(x + w/2, d["Pt_Attack"], w, label="Attack Points", color=PALETTE["blue"],   alpha=0.85)
    ax2.set_yticks(x)
    ax2.set_yticklabels([r["Name"] for _, r in d.iterrows()], fontsize=10)
    ax2.legend(fontsize=9)
    _style_ax(ax2, title="Blocks vs Attacks")
    ax2.grid(axis="x", alpha=0.3, linestyle="--")
    ax2.grid(axis="y", alpha=0)

    fig.suptitle("VNL 2024 Men — Best Middle Blockers", fontsize=14, fontweight="bold", y=1.02)
    fig.tight_layout()
    _save(fig, "06_mb_ranking")


# ---------------------------------------------------------------------------
# 7. Servers
# ---------------------------------------------------------------------------
def plot_servers(srv_df: pd.DataFrame, n: int = 10):
    d = srv_df.head(n).sort_values("Pt_Serve")
    fig, ax = plt.subplots(figsize=(9, 5))
    colors = [PALETTE["red"] if i == len(d)-1 else PALETTE["orange"] for i in range(len(d))]
    bars = ax.barh([f"{r['Name']} ({r['Team']})" for _, r in d.iterrows()],
                   d["Pt_Serve"], color=colors, edgecolor="white")
    for bar, (_, r) in zip(bars, d.iterrows()):
        ax.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height()/2,
                f"{int(r['Pt_Serve'])} pts  ({r['p_Serve']}%)", va="center", fontsize=9)
    ax.set_xlim(0, d["Pt_Serve"].max() * 1.35)
    _style_ax(ax, title="Top 10 Servers — Ace Points\n(label shows efficiency %)", xlabel="Ace Points")
    ax.grid(axis="x", alpha=0.3, linestyle="--")
    ax.grid(axis="y", alpha=0)
    fig.tight_layout()
    _save(fig, "07_top_servers")


# ---------------------------------------------------------------------------
# 8. Position distribution per team — heatmap style
# ---------------------------------------------------------------------------
def plot_position_heatmap(master: pd.DataFrame):
    pivot = (
        master.groupby(["Team", "Position"])
        .size()
        .unstack(fill_value=0)
        .reindex(columns=["OH", "O", "MB", "S", "L"], fill_value=0)
    )
    fig, ax = plt.subplots(figsize=(10, 7))
    im = ax.imshow(pivot.values, aspect="auto", cmap="YlOrRd")
    ax.set_xticks(range(len(pivot.columns)))
    ax.set_xticklabels(pivot.columns, fontsize=11)
    ax.set_yticks(range(len(pivot.index)))
    ax.set_yticklabels(pivot.index, fontsize=11)
    for i in range(pivot.shape[0]):
        for j in range(pivot.shape[1]):
            ax.text(j, i, pivot.values[i, j], ha="center", va="center", fontsize=10)
    plt.colorbar(im, ax=ax, label="Player count")
    ax.set_title("Roster Composition by Position per Team", fontsize=13, fontweight="bold", pad=12)
    fig.tight_layout()
    _save(fig, "08_position_heatmap")


# ---------------------------------------------------------------------------
# 9. Top 20 scorers — summary bar
# ---------------------------------------------------------------------------
def plot_top_scorers(top_df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(12, 7))
    x = np.arange(len(top_df))
    w = 0.6
    b1 = ax.bar(x, top_df["Tot_Atk"],   w, label="Attack",  color=PALETTE["blue"])
    b2 = ax.bar(x, top_df["Tot_Block"],  w, bottom=top_df["Tot_Atk"],
                label="Block", color=PALETTE["green"])
    b3 = ax.bar(x, top_df["Tot_Serve"],  w,
                bottom=top_df["Tot_Atk"] + top_df["Tot_Block"],
                label="Serve", color=PALETTE["orange"])
    ax.set_xticks(x)
    ax.set_xticklabels(
        [f"{r['Name']}\n{r['Team']}" for _, r in top_df.iterrows()],
        rotation=45, ha="right", fontsize=8
    )
    ax.legend(loc="upper right", fontsize=9)
    _style_ax(ax, title="Top 20 Individual Scorers — Points by Phase", ylabel="Points")
    fig.tight_layout()
    _save(fig, "09_top_scorers")


# ---------------------------------------------------------------------------
# 10. Setters
# ---------------------------------------------------------------------------
def plot_setter_ranking(setter_df: pd.DataFrame, n: int = 10):
    d = setter_df.head(n).sort_values("setter_score")
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))

    ax = axes[0]
    ax.hlines(range(len(d)), 0, d["setter_score"], color=PALETTE["blue"], linewidth=1.5, alpha=0.7)
    ax.scatter(d["setter_score"], range(len(d)), color=PALETTE["blue"], s=80, zorder=3)
    ax.set_yticks(range(len(d)))
    ax.set_yticklabels([f"{r['Name']} ({r['Team']})" for _, r in d.iterrows()], fontsize=10)
    _style_ax(ax, title="Setter Score\n(50% vol · 30% efficiency · 20% avg/match)", xlabel="Score (0–100)")
    ax.grid(axis="x", alpha=0.3, linestyle="--")
    ax.grid(axis="y", alpha=0)

    ax2 = axes[1]
    ax2.scatter(d["Sf_Set"], d["p_Set"], s=80, color=PALETTE["blue"], alpha=0.85)
    for _, r in d.iterrows():
        ax2.annotate(r["Name"], (r["Sf_Set"], r["p_Set"]),
                     textcoords="offset points", xytext=(4, 3), fontsize=8)
    _style_ax(ax2, title="Volume vs Efficiency", xlabel="Successful Sets", ylabel="Efficiency %")
    ax2.spines[["top", "right"]].set_visible(False)

    fig.suptitle("VNL 2024 Men — Best Setters", fontsize=14, fontweight="bold", y=1.02)
    fig.tight_layout()
    _save(fig, "10_setter_ranking")



def generate_all(master, rankings, team_df):
    print("\nGenerating plots...")
    plot_team_ranking(team_df)
    plot_team_breakdown(team_df)
    plot_top_attackers(rankings["attackers"])
    plot_attack_scatter(rankings["attackers"])
    plot_libero_ranking(rankings["liberos"])
    plot_mb_ranking(rankings["middle_blockers"])
    plot_servers(rankings["servers"])
    plot_position_heatmap(master)
    plot_top_scorers(rankings["top_scorers"])
    plot_setter_ranking(rankings["setters"])
    print(f"\nAll figures saved to: {OUT_DIR}")


if __name__ == "__main__":
    from data_loader import build_master, team_summary
    from rankings import all_rankings
    master   = build_master()
    rankings = all_rankings(master)
    team_df  = team_summary(master)
    generate_all(master, rankings, team_df)
