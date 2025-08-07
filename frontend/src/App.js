import React, { useState } from "react";
import "./styles.css";

function App() {
  const [ticker, setTicker] = useState("");
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);
  const [file, setFile] = useState(null);
  const [uploadMessage, setUploadMessage] = useState("");

  // Fetch company data
  const fetchData = async () => {
    try {
      const res = await fetch(`https://findocscollector.onrender.com/api/company/${ticker}`);
      const result = await res.json();
      if (res.ok) {
        setData(result);
        setError(null);
      } else {
        setError(result.error);
      }
    } catch (err) {
      setError("Failed to fetch data.");
    }
  };

  // Handle Enter key for ticker search
  const handleKeyPress = (e) => {
    if (e.key === "Enter") {
      fetchData();
    }
  };

  // Handle file upload
  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const uploadFile = async () => {
    if (!file) {
      alert("Please choose a file first");
      return;
    }
    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch(`https://findocscollector.onrender.com/api/upload/`, {
        method: "POST",
        body: formData,
      });
      const result = await res.json();
      if (res.ok) {
        setUploadMessage(`File uploaded successfully: ${result.file_name}`);
      } else {
        setUploadMessage(`Upload failed: ${result.error}`);
      }
    } catch (err) {
      setUploadMessage("Error uploading file.");
    }
  };

  return (
    <div className="container">
      <h1>FinDocsCollector</h1>

      {/* Search box */}
      <div className="search-box">
        <input
          type="text"
          value={ticker}
          placeholder="Enter ticker (e.g., MSFT)"
          onChange={(e) => setTicker(e.target.value)}
          onKeyPress={handleKeyPress}
        />
        <button onClick={fetchData}>Fetch</button>
      </div>

      {/* Upload box */}
      <div className="upload-box">
        <input type="file" onChange={handleFileChange} />
        <button onClick={uploadFile}>Upload to Google Drive</button>
      </div>

      {uploadMessage && <p>{uploadMessage}</p>}

      {/* Results */}
      {data && (
        <div className="results">

          {/* Header with ticker & price */}
          <div className="header">
            <h2>{data.ticker} — ${Number(data.price || 0).toFixed(2)}</h2>
          </div>

          {/* Key data */}
          <section className="key-data">
            <p><strong>7d High:</strong> {data["7d_high"]}</p>
            <p><strong>7d Low:</strong> {data["7d_low"]}</p>
            <p><strong>1m High:</strong> {data["1m_high"]}</p>
            <p><strong>1m Low:</strong> {data["1m_low"]}</p>
            <p><strong>3m High:</strong> {data["3m_high"]}</p>
            <p><strong>3m Low:</strong> {data["3m_low"]}</p>
            <p><strong>1y High:</strong> {data["1y_high"]}</p>
            <p><strong>1y Low:</strong> {data["1y_low"]}</p>
          </section>

          {/* Analytics - directly under Key Data */}
          {data.analytics && (
            <section className="analytics">
              <h2>Analytics</h2>
              <pre>{JSON.stringify(data.analytics, null, 2)}</pre>
            </section>
          )}

          {/* SEC Filings */}
          {data.sec_filings && (
            <section className="sec-filings">
              <h2>SEC Filings</h2>
              <ul>
                {data.sec_filings.map((filing, idx) => (
                  <li key={idx}>
                    <a href={filing.link} target="_blank" rel="noopener noreferrer">
                      {filing.title}
                    </a>{" "}
                    — {filing.date}
                  </li>
                ))}
              </ul>
            </section>
          )}

          {/* News */}
          {data.news && (
            <section className="news">
              <h2>News</h2>
              <ul>
                {data.news.map((story, idx) => (
                  <li key={idx}>
                    <a href={story.link} target="_blank" rel="noopener noreferrer">
                      {story.title}
                    </a>
                  </li>
                ))}
              </ul>
            </section>
          )}
        </div>
      )}

      {error && <p style={{ color: "red" }}>{error}</p>}
    </div>
  );
}

export default App;
