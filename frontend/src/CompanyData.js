import React, { useState } from "react";
import { fetchCompanyData } from "./api";

export default function CompanyData() {
  const [ticker, setTicker] = useState("");
  const [company, setCompany] = useState(null);
  const [error, setError] = useState("");

  const handleFetch = async () => {
    if (!ticker.trim()) return;
    setError("");
    const data = await fetchCompanyData(ticker.trim().toUpperCase());
    if (data) {
      setCompany(data);
    } else {
      setError("Failed to load company data.");
    }
  };

  // ✅ Allow Enter key to trigger fetch
  const handleKeyDown = (e) => {
    if (e.key === "Enter") {
      handleFetch();
    }
  };

  return (
    <div style={{ maxWidth: "800px", margin: "auto", padding: "20px", fontFamily: "Arial, sans-serif" }}>
      <h1>FinDocsCollector</h1>

      <input
        type="text"
        placeholder="Enter ticker (e.g. MSFT)"
        value={ticker}
        onChange={(e) => setTicker(e.target.value)}
        onKeyDown={handleKeyDown}  // ✅ Added this line
        style={{ padding: "8px", marginRight: "10px", width: "200px" }}
      />
      <button onClick={handleFetch} style={{ padding: "8px 16px" }}>Fetch</button>

      {error && <p style={{ color: "red" }}>{error}</p>}

      {company && (
        <div style={{ marginTop: "20px" }}>
          <h2>{company.ticker} - ${company.price || "N/A"}</h2>

          {/* ✅ Expanded Key Data */}
          {company.key_data && (
            <>
              <h3>Key Data</h3>
              <ul>
                <li><strong>7-Day High:</strong> ${company.key_data["7d_high"]}</li>
                <li><strong>7-Day Low:</strong> ${company.key_data["7d_low"]}</li>
                <li><strong>1-Month High:</strong> ${company.key_data["1m_high"]}</li>
                <li><strong>1-Month Low:</strong> ${company.key_data["1m_low"]}</li>
                <li><strong>3-Month High:</strong> ${company.key_data["3m_high"]}</li>
                <li><strong>3-Month Low:</strong> ${company.key_data["3m_low"]}</li>
                <li><strong>1-Year High:</strong> ${company.key_data["1y_high"]}</li>
                <li><strong>1-Year Low:</strong> ${company.key_data["1y_low"]}</li>
              </ul>
            </>
          )}

          {/* ✅ SEC Filings */}
          <h3>SEC Filings</h3>
          {company.sec_filings && company.sec_filings.length > 0 ? (
            <ul>
              {company.sec_filings.map((f, idx) => (
                <li key={idx}>
                  {f.date} - <a href={f.link} target="_blank" rel="noopener noreferrer">{f.title}</a>
                  <br />
                  <small style={{ color: "gray" }}>{f.description}</small>
                </li>
              ))}
            </ul>
          ) : (
            <p>No SEC filings available.</p>
          )}

          {/* ✅ MarketWatch Info */}
          {company.marketwatch && (
            <>
              <h3>MarketWatch: {company.marketwatch.name}</h3>
              <p>MarketWatch Price: ${company.marketwatch.price || "N/A"}</p>
            </>
          )}

          {/* ✅ Latest News */}
          {company.marketwatch?.headlines?.length > 0 && (
            <>
              <h3>Latest News</h3>
              <ul>
                {company.marketwatch.headlines.map((news, i) => (
                  <li key={i}>
                    <a href={news.link} target="_blank" rel="noopener noreferrer">{news.title}</a>
                  </li>
                ))}
              </ul>
            </>
          )}
        </div>
      )}
    </div>
  );
}
