import React from "react";

export default function HistoryList({ items }) {
  if (!items?.length) return <p>No history yet.</p>;

  return (
    <div style={{ border: "1px solid #ddd", padding: 16, borderRadius: 10 }}>
      <h3>Last 5 Uploads</h3>
      <ul>
        {items.map((d) => (
          <li key={d.id || d.uploaded_at}>
            <b>{d.filename}</b> — {new Date(d.uploaded_at).toLocaleString()}
          </li>
        ))}
      </ul>
    </div>
  );
}
