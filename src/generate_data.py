"""
generate_data.py
Generates realistic synthetic manufacturing data for OEE analysis.
Outputs: data/sample_machine_data.csv
"""

import numpy as np
import pandas as pd
from pathlib import Path

SEED = 42
rng = np.random.default_rng(SEED)

MACHINES = [f"M{i:02d}" for i in range(1, 9)]  # M01 – M08
START_DATE = pd.Timestamp("2025-01-01")
END_DATE = pd.Timestamp("2025-06-30")
SHIFTS = ["Day", "Night"]

DOWNTIME_REASONS = [
    "Mechanical Failure",
    "Planned Maintenance",
    "Material Shortage",
    "Operator Break",
    "Changeover",
    "Quality Check Hold",
    "Electrical Fault",
    "None",
]

# Per-machine baseline OEE targets (realistic 60–85% range)
MACHINE_BASELINES = {
    "M01": 0.82,
    "M02": 0.78,
    "M03": 0.75,
    "M04": 0.70,
    "M05": 0.83,
    "M06": 0.65,  # problem machine
    "M07": 0.61,  # worst performer
    "M08": 0.80,
}

# Night shift performs ~10–14% worse than day shift
SHIFT_PENALTY = {"Day": 1.0, "Night": 0.88}

PLANNED_TIME = 480  # minutes per shift (8-hour shift)


def availability(actual_run: float, planned: float) -> float:
    return actual_run / planned


def performance(good_units: int, total_units: int) -> float:
    if total_units == 0:
        return 0.0
    return good_units / total_units


def quality(good_units: int, total_units: int) -> float:
    if total_units == 0:
        return 0.0
    return good_units / total_units


def generate_row(machine_id: str, shift_date: pd.Timestamp, shift: str) -> dict:
    baseline = MACHINE_BASELINES[machine_id]
    penalty = SHIFT_PENALTY[shift]

    # Target OEE for this row (add noise)
    target_oee = baseline * penalty * rng.uniform(0.93, 1.07)
    target_oee = float(np.clip(target_oee, 0.55, 0.92))

    # Availability: 70–98% of planned time actually ran
    availability_rate = rng.uniform(0.70, 0.98)
    actual_run_time = round(PLANNED_TIME * availability_rate)
    downtime_mins = PLANNED_TIME - actual_run_time

    # Downtime reason (None when downtime < 5 mins)
    if downtime_mins < 5:
        downtime_reason = "None"
    else:
        weights = [0.20, 0.18, 0.12, 0.10, 0.15, 0.08, 0.10, 0.07]
        downtime_reason = rng.choice(DOWNTIME_REASONS, p=weights)

    # Units: derive from target OEE back-calculation
    # OEE ≈ availability × quality (simplified model; performance baked into good_units)
    max_units_per_min = rng.uniform(1.8, 2.5)  # machine throughput varies
    total_units = int(actual_run_time * max_units_per_min * rng.uniform(0.90, 1.00))
    quality_rate = target_oee / availability_rate if availability_rate > 0 else 0.80
    quality_rate = float(np.clip(quality_rate, 0.75, 0.99))
    good_units = int(total_units * quality_rate)

    return {
        "machine_id": machine_id,
        "shift_date": shift_date.date(),
        "shift": shift,
        "planned_time_mins": PLANNED_TIME,
        "actual_run_time_mins": actual_run_time,
        "good_units": good_units,
        "total_units": total_units,
        "downtime_mins": downtime_mins,
        "downtime_reason": downtime_reason,
    }


def main():
    dates = pd.date_range(START_DATE, END_DATE, freq="D")
    rows = []

    for date in dates:
        for machine in MACHINES:
            for shift in SHIFTS:
                # Occasional missing shift (~3% chance — realistic data gaps)
                if rng.random() < 0.03:
                    continue
                rows.append(generate_row(machine, date, shift))

    df = pd.DataFrame(rows)

    # Derived OEE columns
    df["availability"] = (df["actual_run_time_mins"] / df["planned_time_mins"]).round(4)
    df["quality"] = (df["good_units"] / df["total_units"]).round(4)
    df["oee"] = (df["availability"] * df["quality"]).round(4)

    out_path = Path(__file__).resolve().parent.parent / "data" / "sample_machine_data.csv"
    out_path.parent.mkdir(exist_ok=True)
    df.to_csv(out_path, index=False)

    print(f"Generated {len(df):,} rows -> {out_path}")
    print(f"\nOEE summary by machine:")
    print(df.groupby("machine_id")["oee"].mean().mul(100).round(1).to_string())
    print(f"\nOEE summary by shift:")
    print(df.groupby("shift")["oee"].mean().mul(100).round(1).to_string())


if __name__ == "__main__":
    main()
