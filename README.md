# 🏐 VNL 2024 Men — Data Analysis

A Python data analysis project exploring the **2024 Volleyball Nations League (Men's Tournament)** using official per-player and team statistics.

Built as a portfolio project targeting **BI Analyst / Data Analyst** roles.

---

## 📂 Project Structure

```
vnl2024-analysis/
├── data/                        # Raw CSV datasets (7 files)
│   ├── VNL2024Men_Players.csv
│   ├── VNL2024Men_Scorers.csv
│   ├── VNL2024Men_Attackers.csv
│   ├── VNL2024Men_Blockers.csv
│   ├── VNL2024Men_Diggers.csv
│   ├── VNL2024Men_Receivers.csv
│   └── VNL2024Men_Servers.csv
├── src/
│   ├── data_loader.py           # Load, clean & merge all 7 CSVs
│   ├── rankings.py              # Composite scoring per position
│   ├── analysis.py              # Team synergy, risk profiles, demographics
│   └── visualisations.py       # All matplotlib charts → outputs/figures/
├── notebooks/
│   └── VNL2024_Analysis.ipynb  # Interactive Jupyter walkthrough
├── outputs/
│   └── figures/                 # Auto-generated PNG charts
├── main.py                      # Full pipeline entry point
├── requirements.txt
└── README.md
```

---

## 🚀 Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/vnl2024-analysis.git
cd vnl2024-analysis

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the full pipeline (loads data → ranks players → generates 9 charts)
python main.py

# Optional flags
python main.py --no-plots       # skip chart generation
python main.py --export-csv     # also export ranked CSVs to outputs/csv/
```

---

## 📊 What's Analysed

### Team Level
| Analysis | Description |
|---|---|
| Team Rankings | Total points scored across all phases |
| Points Breakdown | Attack / Block / Serve contribution per team |
| Team Synergy | Balance score — how evenly distributed are a team's points? |

### Player Level — Composite Scoring

Each position is judged by metrics relevant to their role:

#### 🏆 Best Attacker
> All positions (O, OH, MB) with significant attack volume

| Component | Weight |
|---|---|
| Attack Points (volume) | 50% |
| Attack Efficiency % | 30% |
| Average per Match | 20% |

**Winner: T. Stern (SLO) — 265 pts, 54.5% efficiency**

---

#### 🛡️ Best Libero
> Position = L only — judged on combined defence

| Component | Weight |
|---|---|
| Successful Digs | 40% |
| Dig Efficiency % | 30% |
| Successful Receives | 40% |
| Receive Efficiency % | 30% |

**Winner: Kovacic (SLO) — best all-round defender**

---

#### 🧱 Best Middle Blocker
> Position = MB — attack and blocking combined

| Component | Weight |
|---|---|
| Block Points | 50% |
| Attack Points | 30% |
| Attack Efficiency % | 20% |

**Winner: Concepcion (CUB) — exceptional 63.6% attack efficiency for an MB**

---

#### 💥 Best Server
> Ranked by ace points, secondary by efficiency %

**Winner: Nimir (NED) — 40 ace points at 21% efficiency**

---

## 📈 Generated Charts

| # | File | Description |
|---|---|---|
| 1 | `01_team_ranking.png` | Horizontal bar — team total points |
| 2 | `02_team_breakdown.png` | Stacked bar — attack/block/serve per team |
| 3 | `03_top_attackers.png` | Lollipop — top 10 by composite score |
| 4 | `04_attack_scatter.png` | Scatter — volume vs efficiency by position |
| 5 | `05_libero_ranking.png` | Combined defence score + digs vs receives |
| 6 | `06_mb_ranking.png` | MB composite score + blocks vs attacks |
| 7 | `07_top_servers.png` | Ace points + efficiency % |
| 8 | `08_position_heatmap.png` | Roster composition heatmap by team |
| 9 | `09_top_scorers.png` | Top 20 individual scorers stacked by phase |

---

## 🔑 Key Findings

- **France** topped the tournament in total points (1025), attack points (807), and block points (138)
- **Slovenia** led in serve points (106) and had the top two individual scorers (T. Stern + Cebulj)
- **T. Stern (SLO)** is the best attacker by volume; **Nimir (NED)** is the best per match
- **Kovacic (SLO)** is the best all-round libero; **Danani (ARG)** digs the most
- **Concepcion (CUB)** is the surprise best MB — unusually high attack efficiency for the position
- **GER** had the worst block-to-attack ratio — mostly relying on attack with little defensive phase contribution

---

## 🛠️ Tech Stack

- **Python 3.10+**
- **pandas** — data loading, cleaning, merging, groupby aggregations
- **numpy** — normalisation and numerical operations
- **matplotlib** — all visualisations
- **Jupyter Notebook** — interactive analysis walkthrough

---

## 📁 Data Source

Official VNL 2024 statistics exported from the FIVB/VNL statistical platform.  
16 teams · 304 players · 7 statistical categories (attack, block, serve, dig, receive, scoring, roster)

---

## 👤 Author

Made by [Your Name] · [LinkedIn] · [Portfolio]
