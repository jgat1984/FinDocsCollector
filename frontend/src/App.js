import React, { useState } from "react";

function App() {
  const [ticker, setTicker] = useState("");
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);
  const [file, setFile] = useState(null);
  const [uploadMessage, setUploadMessage] = useState("");

  // Fetch company data
  const fetchData = async () => {
    if (!ticker) return;
    try {
      //const response = await fetch(`/api/company/${ticker}/`); old version
      const res = await fetch(`https://findocscollector.onrender.com/api/company/${ticker}`);
      if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
      const json = await response.json();
      console.log("API Response:", json);
      setData(json);
      setError(null);
    } catch (err) {
      console.error("Fetch Error:", err);
      setError("Failed to fetch data. Check backend logs.");
    }
  };

  // Download JSON
  const downloadJSON = () => {
    if (!data) return;
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `${ticker}_analysis.json`;
    a.click();
  };

  // File selection
  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  // Upload to Google Drive
  const handleUpload = async (e) => {
  e.preventDefault();
  if (!file) {
    alert("Please select a file first.");
    return;
  }

  const formData = new FormData();
  formData.append("file", file);

  try {
    //const res = await fetch("/api/upload/", { method: "POST", body: formData }); old program
    const res = await fetch("https://findocscollector.onrender.com/api/upload/", { method: "POST", body: formData });

    const text = await res.text(); // ✅ Get raw text first

    let result;
    try {
      result = JSON.parse(text); // ✅ Try parsing JSON
    } catch {
      console.error("[DEBUG] Non-JSON response from backend:", text);
      throw new Error("Backend returned HTML instead of JSON. Check server logs.");
    }

    if (res.ok) {
      setUploadMessage(`✅ ${result.message || "File uploaded successfully"} (File ID: ${result.file_id || result.fileId || "N/A"})`);
    } else {
      setUploadMessage(`❌ Upload failed: ${result.error || "Unknown error"}`);
    }
  } catch (err) {
    setUploadMessage(`❌ Upload failed: ${err.message}`);
  }
};



  return (
    <div className="container">
      <h1>FinDocsCollector</h1>

      {/* Search */}
      <input
        type="text"
        placeholder="Enter ticker..."
        value={ticker}
        onChange={(e) => setTicker(e.target.value)}
        onKeyDown={(e) => e.key === "Enter" && fetchData()}
      />
      <button onClick={fetchData}>Fetch</button>

      {/* Upload */}
      <div style={{ marginTop: "15px" }}>
        <input type="file" onChange={handleFileChange} />
        <button onClick={handleUpload}>Upload to Google Drive</button>
        {uploadMessage && <p><strong>{uploadMessage}</strong></p>}
      </div>

      {/* Errors */}
      {error && <p style={{ color: "red" }}>{error}</p>}

      {/* Results */}
      {data ? (
        <div className="results">
          <h2>{data.ticker} – ${data.price ?? "N/A"}</h2>

          {/* ✅ Price Ranges Table */}
          <h3>Price Ranges</h3>
          <table border="1" cellPadding="5" style={{ borderCollapse: "collapse", width: "100%" }}>
            <thead>
              <tr>
                <th>Period</th>
                <th>High</th>
                <th>Low</th>
              </tr>
            </thead>
            <tbody>
              <tr><td>7d</td><td>{data["7d_high"] ?? "-"}</td><td>{data["7d_low"] ?? "-"}</td></tr>
              <tr><td>1m</td><td>{data["1m_high"] ?? "-"}</td><td>{data["1m_low"] ?? "-"}</td></tr>
              <tr><td>3m</td><td>{data["3m_high"] ?? "-"}</td><td>{data["3m_low"] ?? "-"}</td></tr>
              <tr><td>1y</td><td>{data["1y_high"] ?? "-"}</td><td>{data["1y_low"] ?? "-"}</td></tr>
            </tbody>
          </table>

          {/* ✅ Analytics Table */}
          {data.analytics && (
            <div>
              <h3>Analytics</h3>
              <table border="1" cellPadding="5" style={{ borderCollapse: "collapse", width: "100%" }}>
                <thead>
                  <tr>
                    <th>Trend</th>
                    <th>Average High</th>
                    <th>Average Low</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td>{data.analytics.trend || "-"}</td>
                    <td>{data.analytics.average_high || data.analytics.avg_high || "-"}</td>
                    <td>{data.analytics.average_low || data.analytics.avg_low || "-"}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          )}

          {data.last_updated && <p><em>Last Updated: {data.last_updated}</em></p>}

          {/* SEC Filings */}
          <h3>SEC Filings</h3>
          <ul>
            {data.sec_filings?.length ? (
              data.sec_filings.map((f, i) => (
                <li key={i}><a href={f.link} target="_blank" rel="noreferrer">{f.title}</a> ({f.date})</li>
              ))
            ) : <li>No filings available.</li>}
          </ul>

          {/* Market News */}
          <h3>Market News</h3>
          <ul>
            {data.market_news?.length ? (
              data.market_news.map((n, i) => (
                <li key={i}><a href={n.link} target="_blank" rel="noreferrer">{n.title}</a></li>
              ))
            ) : <li>No news available.</li>}
          </ul>

          {/* Earnings Transcript */}
          <h3>Earnings Call Transcript</h3>
          <p>{data.earnings_transcript?.summary ?? "Transcript not available."}</p>
          {data.earnings_transcript?.link && (
            <p><a href={data.earnings_transcript.link} target="_blank" rel="noreferrer">Read full transcript</a></p>
          )}

          {/* Download */}
          <button onClick={downloadJSON}>Download JSON</button>
        </div>
      ) : (
        <p>Enter a ticker and click Fetch to see results.</p>
      )}
    </div>
  );
}

export default App;
