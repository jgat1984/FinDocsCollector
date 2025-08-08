import React, { useState } from "react";
import "./styles.css";

function App() {
  const [ticker, setTicker] = useState("");
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

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

  const downloadJSON = () => {
    if (!data) return;
    const blob = new Blob([JSON.stringify(data, null, 2)], {
      type: "application/json",
    });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `${ticker}_data.json`;
    a.click();
  };

  return (
    <div className="container">
      <h1>FinDocsCollector</h1>

      <div className="search-box">
        <input
          type="text"
          placeholder="Enter ticker..."
          value={ticker}
          onChange={(e) => setTicker(e.target.value)}
          onKeyPress={(e) => e.key === "Enter" && fetchData()}
        />
        <button onClick={fetchData}>Fetch</button>
        <button onClick={downloadJSON}>Download JSON</button>
      </div>

      {/* Hidden Upload UI */}
      <div className="upload-box hidden">
        <input type="file" onChange={() => {}} />
        <button>Upload to Google Drive</button>
      </div>

      {error && <p style={{ color: "red" }}>{error}</p>}

      {data && (
        <>
          <h2>{data.ticker} – ${data.price}</h2>

          <h3>Price Ranges</h3>
          <table>
            <thead>
              <tr>
                <th>Period</th>
                <th>High</th>
                <th>Low</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>7d</td>
                <td>{data["7d_high"]}</td>
                <td>{data["7d_low"]}</td>
              </tr>
              <tr>
                <td>1m</td>
                <td>{data["1m_high"]}</td>
                <td>{data["1m_low"]}</td>
              </tr>
              <tr>
                <td>3m</td>
                <td>{data["3m_high"]}</td>
                <td>{data["3m_low"]}</td>
              </tr>
              <tr>
                <td>1y</td>
                <td>{data["1y_high"]}</td>
                <td>{data["1y_low"]}</td>
              </tr>
            </tbody>
          </table>

          <h3>Analytics</h3>
          <table>
            <thead>
              <tr>
                <th>Average High</th>
                <th>Average Low</th>
                <th>Trend</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>{data.avg_high}</td>
                <td>{data.avg_low}</td>
                <td>{data.trend}</td>
              </tr>
            </tbody>
          </table>
        </>
      )}
    </div>
  );
}

export default App;
