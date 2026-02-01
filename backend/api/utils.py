import pandas as pd

REQUIRED_COLS = ["Equipment Name", "Type", "Flowrate", "Pressure", "Temperature"]

SAFE_RANGES = {
    "Flowrate": (50, 300),
    "Pressure": (10, 60),
    "Temperature": (20, 130),
}

def _penalty(value, low, high):
    if pd.isna(value):
        return 10
    if low <= value <= high:
        return 0
    if value < low:
        return (low - value) / (high - low + 1e-9) * 100
    return (value - high) / (high - low + 1e-9) * 100


def analyze_csv(csv_file):
    df = pd.read_csv(csv_file)

    # Normalize column names (if user has extra spaces)
    df.columns = [c.strip() for c in df.columns]

    # Validate required columns
    missing = [c for c in REQUIRED_COLS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    # Ensure numeric columns are numeric (avoid string issues)
    for col in ["Flowrate", "Pressure", "Temperature"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    summary = {
        "total_equipment": int(len(df)),
        "avg_flowrate": float(df["Flowrate"].mean()),
        "avg_pressure": float(df["Pressure"].mean()),
        "avg_temperature": float(df["Temperature"].mean()),
        "type_distribution": df["Type"].value_counts().to_dict(),
    }

    alerts = []
    scores = []

    for _, row in df.iterrows():
        name = str(row.get("Equipment Name", "Unknown"))
        eq_type = str(row.get("Type", "Unknown"))

        penalties = []
        for col, (low, high) in SAFE_RANGES.items():
            val = row.get(col)
            p = _penalty(val, low, high)
            penalties.append(p)

            if p > 0:
                if pd.isna(val):
                    alerts.append({
                        "equipment": name,
                        "type": eq_type,
                        "metric": col,
                        "issue": "missing"
                    })
                elif val < low:
                    alerts.append({
                        "equipment": name,
                        "type": eq_type,
                        "metric": col,
                        "issue": "low",
                        "value": float(val),
                        "limit": low
                    })
                else:
                    alerts.append({
                        "equipment": name,
                        "type": eq_type,
                        "metric": col,
                        "issue": "high",
                        "value": float(val),
                        "limit": high
                    })

        score = max(0, 100 - (sum(penalties) / len(penalties)))
        scores.append(score)

    health_score = float(sum(scores) / len(scores)) if scores else 0.0

    def bucket(s):
        if s >= 80: return "Good"
        if s >= 50: return "Moderate"
        return "Critical"

    bucket_counts = {}
    for s in scores:
        b = bucket(s)
        bucket_counts[b] = bucket_counts.get(b, 0) + 1

    summary["health_score"] = round(health_score, 2)
    summary["risk_buckets"] = bucket_counts
    summary["alerts"] = alerts[:50]

    return summary
