import React from "react";
import { Bar } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

export default function TypeBarChart({ summary }) {
  const dist = summary?.type_distribution || {};
  const labels = Object.keys(dist);
  const values = Object.values(dist);

  if (!labels.length) return <p>No chart data yet. Upload a CSV.</p>;

  const data = {
    labels,
    datasets: [
      {
        label: "Count",
        data: values,
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: { legend: { display: true }, title: { display: true, text: "Equipment Type Distribution" } },
  };

  return (
    <div style={{ border: "1px solid #ddd", padding: 16, borderRadius: 10 }}>
      <Bar data={data} options={options} />
    </div>
  );
}
