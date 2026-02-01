import React, { useEffect, useState } from "react";
import { getSummary, getHistory, uploadCSV } from "../services/api";

export default function Dashboard() {
  const [summary, setSummary] = useState(null);
  const [historyData, setHistoryData] = useState([]);
  const [trend, setTrend] = useState("Unknown");
  const [file, setFile] = useState(null);

  async function loadData() {
    try {
      const s = await getSummary();
      setSummary(s);

      const h = await getHistory();
      setHistoryData(h.history || h); // supports both formats
      setTrend(h.trend || "Unknown");
    } catch (e) {
      alert("Backend not reachable / API error");
      console.error(e);
    }
  }

  useEffect(() => {
    loadData();
  }, []);

  async function handleUpload() {
    if (!file) {
      alert("Select a CSV file first!");
      return;
    }
    try {
      await uploadCSV(file);
      alert("Upload successful ✅");
      setFile(null);
      await loadData();
    } catch (e) {
      alert("Upload failed: " + e.message);
      console.error(e);
    }
  }

  const alertsCount = summary?.alerts?.length || 0;

  return (
    <div style={{ padding: 30 }}>
      <h1>Chemical Equipment Dashboard</h1>

      <div style={{ display: "flex", gap: 12, alignItems: "center", marginBottom: 16 }}>
        <button onClick={loadData}>Refresh</button>

        <input
          type="file"
          accept=".csv"
          onChange={(e) => setFile(e.target.files?.[0] || null)}
        />
        <button onClick={handleUpload}>Upload CSV</button>
      </div>

      <div style={{ marginTop: 10 }}>
        <b>Trend:</b> {trend}
      </div>

      <div style={{ marginTop: 10 }}>
        {alertsCount === 0 ? (
          <span>No alerts ✅</span>
        ) : (
          <span style={{ color: "red" }}>Alerts: {alertsCount}</span>
        )}
      </div>

      <h3 style={{ marginTop: 20 }}>Summary</h3>
      {!summary ? (
        <div>No summary yet</div>
      ) : (
        <div style={{ display: "flex", gap: 12, flexWrap: "wrap" }}>
          <Card title="Total Equipment" value={summary.total_equipment} />
          <Card title="Avg Flowrate" value={summary.avg_flowrate} />
          <Card title="Avg Pressure" value={summary.avg_pressure} />
          <Card title="Avg Temperature" value={summary.avg_temperature} />
          <Card title="Health Score" value={summary.health_score ?? "-"} />
        </div>
      )}

      {/* ✅ ALERTS LIST (added correctly inside return) */}
      {summary?.alerts?.length > 0 && (
        <>
          <h3 style={{ marginTop: 25 }}>Alerts</h3>
          <ul>
            {summary.alerts.map((a, i) => (
              <li key={i}>
                <b>{a.equipment}</b> — {a.metric} — {a.issue}
                {a.value !== undefined ? ` (value: ${a.value})` : ""}
                {a.limit !== undefined ? ` (limit: ${a.limit})` : ""}
              </li>
            ))}
          </ul>
        </>
      )}

      <h3 style={{ marginTop: 25 }}>Upload History</h3>
      {historyData?.length ? (
        <ul>
          {historyData.map((item) => (
            <li key={item.id}>
              {item.filename} — {new Date(item.uploaded_at).toLocaleString()}
            </li>
          ))}
        </ul>
      ) : (
        <div>No history yet</div>
      )}
    </div>
  );
}

function Card({ title, value }) {
  return (
    <div
      style={{
        border: "1px solid #ddd",
        padding: 14,
        borderRadius: 10,
        minWidth: 180,
      }}
    >
      <b>{title}</b>
      <div>{value ?? "-"}</div>
    </div>
  );
}
