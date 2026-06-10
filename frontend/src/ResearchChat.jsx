import { useState } from "react";
import axios from "axios";

export default function ResearchChat() {
  const [query, setQuery] = useState("");
  const [summary, setSummary] = useState("");
  const [localPapers, setLocalPapers] = useState([]);
  const [pubmedPapers, setPubmedPapers] = useState([]);
  const [loading, setLoading] = useState(false);

  const searchResearch = async () => {
    if (!query.trim()) return;

    setLoading(true);
    setSummary("");
    setLocalPapers([]);
    setPubmedPapers([]);

    try {
      const res = await axios.get("http://127.0.0.1:8000/research-chat", {
        params: { query },
      });

      setSummary(res.data.summary);
      setLocalPapers(res.data.local_papers || []);
      setPubmedPapers(res.data.pubmed_papers || []);
    } catch (error) {
      console.error(error);
      setSummary("Unable to connect to backend.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="research-card">
      <div className="section-title">
        <h2>Healthcare Research Assistant</h2>
        <p>Search local papers and PubMed abstracts</p>
      </div>

      <div className="search-box">
        <input
          type="text"
          placeholder="Example: AI in healthcare"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <button onClick={searchResearch}>Search</button>
      </div>

      {loading && <div className="status-card">Searching research papers...</div>}

      {summary && (
        <div className="result-section">
          <h3>Research Summary</h3>
          <div className="summary-card">{summary}</div>
        </div>
      )}

      {localPapers.length > 0 && (
        <div className="result-section">
          <h3>Local Recommended Papers</h3>
          <div className="paper-list">
            {localPapers.map((paper, index) => (
              <div className="paper-card" key={index}>
                <span className="paper-rank">{index + 1}</span>
                <span>{paper}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {pubmedPapers.length > 0 && (
        <div className="result-section">
          <h3>PubMed Papers</h3>
          <div className="paper-list">
            {pubmedPapers.map((paper, index) => (
              <div className="pubmed-card" key={index}>
                <h4>{index + 1}. {paper.title}</h4>
                <p><strong>Journal:</strong> {paper.journal}</p>
                <p><strong>PMID:</strong> {paper.pmid}</p>
                <p><strong>Date:</strong> {paper.pub_date}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}