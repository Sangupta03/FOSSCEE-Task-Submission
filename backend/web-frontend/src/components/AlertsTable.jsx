import React from "react";

export default function AlertsTable({ alerts = [] }) {
  if (!alerts.length) return <div style={{ marginTop: 16 }}>No alerts ✅</div>;

  return (
    <div style={{ marginTop: 16 }}>
      <h3>Alerts ({alerts.length})</h3>
      <table style={{ width: "100%", borderCollapse: "collapse" }} border="1" cellPadding="8">
        <thead>
          <tr>
            <th>Equipment</th>
            <th>Type</th>
            <th>Metric</th>
            <th>Issue</th>
            <th>Value</th>
            <th>Limit</th>
          </tr>
        </thead>
        <tbody>
          {alerts.map((a, i) => (
            <tr key={i}>
              <td>{a.equipment}</td>
              <td>{a.type}</td>
              <td>{a.metric}</td>
              <td>{a.issue}</td>
              <td>{a.value ?? "-"}</td>
              <td>{a.limit ?? "-"}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
