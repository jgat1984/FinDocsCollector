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
      const res = await fetch(`/api/company/${ticker}`);
      const result = await res.json();
      if (res.ok) {
        setData(result);
        setError(null);
      } else {
        setError(result.error);
        setData(null);
      }
    } catch (err) {
      setError("Failed to fetch data.");
    }
  };

  const handleFileUpload = async () => {
    if (!file) return;
    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch("/api/upload/", {
        method: "POST",
        body: formData
      });
      const result = await res.json();
      if (res.ok) {
        setUploadMessage("File uploaded successfully!");
      } else {
        setUploadMessage(result.error || "Upload failed");
      }
    } catch (err) {
      setUploadMessage("Error uploading file.");
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter") fetchData();
  };

  return (
    <div className="container">
      <h1>FinDocsCollector</h1>

      <div className="search-box">
        <input
          type="text"
          placeholder="Enter stock ticker"
          value={ticker}
          onChange={(e) => setTicker(e.target.value)}
          onKeyDown={handleKeyPress}
        />
        <button onClick={fetchData}>Fetch</button>
      </div>

      {error && <p style={{ color: "red" }}>{error}</p>}

      {data && (
        <div className="results">
          <h2>{data.ticker}</h2>
          <p><strong>Price:</strong> ${data.price}</p>

          <div className="key-data">
            <p><strong>7D High:</strong> {data["7d_high"]}</p>
            <p><strong>7D Low:</strong> {data["7d_low"]}</p>
            <p><strong>1M High:</strong> {data["1m_high"]}</p>
            <p><strong>1M Low:</strong> {data["1m_low"]}</p>
            <p><strong>3M High:</strong> {data["3m_high"]}</p>
            <p><strong>3M Low:</strong> {data["3m_low"]}</p>
            <p><strong>1Y High:</strong> {data["1y_high"]}</p>
            <p><strong>1Y Low:</strong> {data["1y_low"]}</p>
          </div>

          <div className="analytics">
            {data.analytics && <pre>{JSON.stringify(data.analytics, null, 2)}</pre>}
          </div>

          <div className="sec-filings">
            <h3>SEC Filings</h3>
            <ul>
              {data.sec_filings.map((f, idx) => (
                <li key={idx}><a href={f.link} target="_blank" rel="noreferrer">{f.title}</a> — {new Date(f.date).toLocaleDateString()}</li>
              ))}
            </ul>
          </div>

          <div className="news">
            <h3>Market News</h3>
            <ul>
              {data.market_news.map((n, idx) => (
                <li key={idx}><a href={n.link} target="_blank" rel="noreferrer">{n.title}</a></li>
              ))}
            </ul>
          </div>

          <div className="transcript">
            <h3>Earnings Transcript</h3>
            <p>{data.earnings_transcript.summary}</p>
            <a href={data.earnings_transcript.link} target="_blank" rel="noreferrer">Read full transcript</a>
          </div>
        </div>
      )}

      <div className="upload-box">
        <input type="file" onChange={(e) => setFile(e.target.files[0])} />
        <button onClick={handleFileUpload}>Upload to Drive</button>
      </div>
      {uploadMessage && <p>{uploadMessage}</p>}
    </div>
  );
}

export default App;
