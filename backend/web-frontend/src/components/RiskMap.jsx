export default function RiskMap({ buckets }) {
  if (!buckets) return null;

  const colors = { Good: "green", Moderate: "orange", Critical: "red" };

  return (
    <div style={{ marginTop: 16 }}>
      <h3>Risk Map</h3>
      {Object.entries(buckets).map(([k, v]) => (
        <div key={k} style={{ color: colors[k] || "black", fontWeight: "bold" }}>
          {k}: {v}
        </div>
      ))}
    </div>
  );
}
