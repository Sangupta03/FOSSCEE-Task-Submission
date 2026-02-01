import React, { useState } from "react";
import { uploadCSV } from "../services/api";

export default function UploadForm({ onUploaded }) {
  const [file, setFile] = useState(null);
  const [msg, setMsg] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) return setMsg("Please choose a CSV file.");

    try {
      setMsg("Uploading...");
      const res = await uploadCSV(file);
      setMsg("Upload successful!");
      onUploaded?.(res.data); // trigger refresh on dashboard
    } catch (err) {
      setMsg(err?.response?.data?.error || "Upload failed");
    }
  };

  return (
    <div style={{ border: "1px solid #ddd", padding: 16, borderRadius: 10 }}>
      <h3>Upload CSV</h3>
      <form onSubmit={handleSubmit}>
        <input
          type="file"
          accept=".csv"
          onChange={(e) => setFile(e.target.files?.[0] || null)}
        />
        <button style={{ marginLeft: 10 }} type="submit">
          Upload
        </button>
      </form>
      {msg && <p style={{ marginTop: 10 }}>{msg}</p>}
    </div>
  );
}
