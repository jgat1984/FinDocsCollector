import React, { useState } from "react";
import "./styles.css";

function App() {
  const [ticker, setTicker] = useState("");
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);
  const [file, setFile] = useState(null);
  const [uploadMessage, setUploadMessage] = useState("");

  const fetchData = async () => {
    try {
      const response = await fetch(`https://findocscollector.onrender.com/api/company/${ticker}`);
      const result = await response.json();
      if (response.ok) {
        setData(result);
        setError(null);
      } else {
        setError(result.error);
      }
    } catch (err) {
      setError("Failed to fetch data.");
    }
  };

  const downloadJSON = () => {
    if (!data) return;
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `${ticker}_data.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const handleUpload = async () => {
    if (!file) return;
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("https://findocscollector.onrender.com/api/upload/", {
        method: "POST",
        body: formData,
      });

      const result = await response.json();
      if (response.ok) {
        setUploadMessage(result.message + " ✅");
      } else {
        setUploadMessage(result.error || "Upload failed.");
      }
    } catch (err) {
      setUploadMessage("Upload failed: " + err.message);
    }
  };

  return (
    <div className="container">
      <h1>FinDocsCollector</h1>

      <input
        type="text"
        value={ticker}
        onChange={(e) => setTicker(e.target.value)}
        onKeyDown={(e) => e.key === "Enter" && fetchData()}
        placeholder="Enter ticker symbol (e.g., MSFT)"
      />
      <button onClick={fetchData}>Fetch</button>
      <button onClick={downloadJSON} disabled={!data}>Download JSON</button>

      <div>
        <input type="file" onChange={(e) => setFile(e.target.files[0])} />
        <button onClick={handleUpload}>Upload to Google Drive</button>
        {uploadMessage && <p className="upload-message">{uploadMessage}</p>}
      </div>

      {error && <p className="error">{error}</p>}

      {data && (
        <div className="results">
          <h2>{data.ticker} – ${Number(data.price || 0).toFixed(2)}</h2>

          <h3>Price Ranges</h3>
          <table>
            <thead>
              <tr><th>Period</th><th>High</th><th>Low</th></tr>
            </thead>
            <tbody>
              <tr><td>7d</td><td>{data["7d_high"]}</td><td>{data["7d_low"]}</td></tr>
              <tr><td>1m</td><td>{data["1m_high"]}</td><td>{data["1m_low"]}</td></tr>
              <tr><td>3m</td><td>{data["3m_high"]}</td><td>{data["3m_low"]}</td></tr>
              <tr><td>1y</td><td>{data["1y_high"]}</td><td>{data["1y_low"]}</td></tr>
            </tbody>
          </table>

          {data.analytics && (
            <>
              <h3>Analytics</h3>
              <table>
                <thead>
                  <tr><th>Average High</th><th>Average Low</th><th>Trend</th></tr>
                </thead>
                <tbody>
                  <tr>
                    <td>{data.analytics.average_high}</td>
                    <td>{data.analytics.average_low}</td>
                    <td>{data.analytics.trend}</td>
                  </tr>
                </tbody>
              </table>
            </>
          )}

          <h3>SEC Filings</h3>
          <ul>
            {data.sec_filings.map((filing, idx) => (
              <li key={idx}>
                <a href={filing.link} target="_blank" rel="noreferrer">
                  {filing.title} ({filing.date})
                </a>
              </li>
            ))}
          </ul>

          <h3>Market News</h3>
          <ul>
            {data.market_news.map((item, idx) => (
              <li key={idx}>
                <a href={item.link} target="_blank" rel="noreferrer">
                  {item.title}
                </a>
              </li>
            ))}
          </ul>

          {data.earnings_transcript && (
            <>
              <h3>Earnings Transcript</h3>
              <p>{data.earnings_transcript.summary}</p>
              <a href={data.earnings_transcript.link} target="_blank" rel="noreferrer">
                View Full Transcript
              </a>
            </>
          )}
        </div>
      )}
    </div>
  );
}

export default App;
