# 🏭 Manufacturing OEE Analytics Dashboard

An end-to-end data analytics project — from raw industrial sensor data to an interactive Power BI dashboard tracking **Overall Equipment Effectiveness (OEE)** across machines and production shifts.

> OEE = Availability × Performance × Quality
> The gold standard metric in manufacturing analytics.

---

## 📌 What this project does

Most manufacturing teams track OEE manually in Excel — slow, error-prone, and always out of date. This project automates the entire pipeline:

1. **Raw sensor data** (CSV exports from industrial machines)
2. **Python cleaning** — handles missing readings, timestamp errors, outliers
3. **SQL analysis** — calculates OEE components, ranks downtime causes, tracks trends
4. **Power BI dashboard** — shift-level view, machine comparison, week-over-week trends

---

## 📊 Dashboard features

- Overall OEE % by machine and by shift
- Top 5 downtime causes (ranked by lost production time)
- Week-over-week performance trend
- Availability, Performance, and Quality breakdown per line

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python (Pandas, NumPy) | Data cleaning & transformation |
| SQL (CTEs, Window Functions) | OEE calculations & trend analysis |
| Power BI (DAX) | Dashboard & visualisation |
| Matplotlib | EDA & exploratory charts |

---

## 📁 Project Structure

```
oee-dashboard/
│
├── data/
│   └── sample_machine_data.csv      # Sample dataset
│
├── notebooks/
│   └── 01_eda_and_cleaning.ipynb    # Exploratory analysis & cleaning
│   └── 02_oee_calculations.ipynb    # OEE metric derivation
│
├── sql/
│   └── oee_queries.sql              # All SQL queries used
│
├── dashboard/
│   └── oee_dashboard.pbix           # Power BI file
│
└── README.md
```

---

## 🔍 Key SQL Concepts Used

- **CTEs** for multi-step OEE calculation
- **Window functions** (RANK, LAG) for downtime ranking and trend comparison
- **CASE statements** for shift segmentation
- **Aggregations** across machine_id, shift_date dimensions

---

## 💡 Key Insights Found

- Machine downtime was concentrated in 2 out of 8 machines (80/20 rule holds)
- Night shift consistently underperformed day shift by ~12% OEE
- Planned maintenance windows were poorly timed — 40% occurred during high-demand periods

---

## 🚀 How to run

```bash
git clone https://github.com/cosmicskull711/oee-dashboard
cd oee-dashboard
pip install -r requirements.txt
jupyter notebook notebooks/01_eda_and_cleaning.ipynb
```

---

## 👤 Author

**Harsh Dubey** — [LinkedIn](https://www.linkedin.com/in/harsh-dubey-1b169a242) · [GitHub](https://github.com/cosmicskull711)
