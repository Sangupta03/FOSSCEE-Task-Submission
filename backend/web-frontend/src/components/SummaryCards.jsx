import React from "react";

export default function SummaryCards({ summary }) {
  if (!summary) return null;

  const cardStyle = {
    border: "1px solid #ddd",
    padding: 14,
    borderRadius: 10,
    minWidth: 180,
  };

  return (
    <div style={{ display: "flex", gap: 12, flexWrap: "wrap" }}>
      <div style={cardStyle}>
        <b>Total Equipment</b>
        <div>{summary.total_equipment ?? "-"}</div>
      </div>

      <div style={cardStyle}>
        <b>Avg Flowrate</b>
        <div>{summary.avg_flowrate?.toFixed?.(2) ?? summary.avg_flowrate ?? "-"}</div>
      </div>

      <div style={cardStyle}>
        <b>Avg Pressure</b>
        <div>{summary.avg_pressure?.toFixed?.(2) ?? summary.avg_pressure ?? "-"}</div>
      </div>

      <div style={cardStyle}>
        <b>Avg Temperature</b>
        <div>{summary.avg_temperature?.toFixed?.(2) ?? summary.avg_temperature ?? "-"}</div>
      </div>

      <div style={cardStyle}>
        <b>Health Score</b>
        <div>{summary.health_score ?? "-"}</div>
      </div>
    </div>
  );
}
