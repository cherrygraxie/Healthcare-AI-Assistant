import { useState } from "react";
import axios from "axios";
import "./Chat.css";

export default function Chat() {
  const [mode, setMode] = useState("chat");
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);
  const [file, setFile] = useState(null);
  const [uploadMessage, setUploadMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const uploadPDF = async () => {
    if (!file) {
      alert("Please select a PDF first");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await axios.post("http://127.0.0.1:8000/upload", formData);
      setUploadMessage(`PDF uploaded successfully | Chunks: ${res.data.chunks}`);
    } catch (error) {
      console.error(error);
      setUploadMessage("PDF upload failed");
    }
  };

  const sendMessage = async () => {
    if (!input.trim()) return;

    const question = input;

    setMessages((prev) => [
      ...prev,
      { role: "user", text: question, healthData: {} },
    ]);

    setInput("");
    setLoading(true);

    try {
      if (mode === "research") {
        const res = await axios.get("http://127.0.0.1:8000/research-chat", {
          params: { query: question },
        });

        const papers = res.data.pubmed_papers
          ?.map(
            (p, i) =>
              `${i + 1}. ${p.title}\nPMID: ${p.pmid}\nJournal: ${p.journal}\nDate: ${p.pub_date}`
          )
          .join("\n\n");

        setMessages((prev) => [
          ...prev,
          {
            role: "bot",
            text: `${res.data.summary}\n\nRecommended PubMed Papers:\n${
              papers || "No PubMed papers found."
            }`,
            healthData: {},
          },
        ]);
      } else {
        const res = await axios.get("http://127.0.0.1:8000/agent-chat", {
          params: { question },
        });

        setMessages((prev) => [
          ...prev,
          {
            role: "bot",
            text: res.data.answer,
            healthData: res.data.health_data || {},
          },
        ]);
      }
    } catch (error) {
      console.error(error);

      setMessages((prev) => [
        ...prev,
        {
          role: "bot",
          text: "Sorry, I could not get a response from the backend.",
          healthData: {},
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const renderHealthCards = (healthData) => {
    if (!healthData) return null;

    return (
      <>
        {healthData.abnormal?.length > 0 && (
          <div className="health-section abnormal">
            <h3>Abnormal Results</h3>

            {healthData.abnormal.map((item, index) => (
              <div className="health-card" key={`abnormal-${index}`}>
                <h4>{item.test}</h4>
                <p>
                  Value: {item.value} {item.unit}
                </p>
                <p>Range: {item.range}</p>
                <strong>Status: {item.status}</strong>
              </div>
            ))}
          </div>
        )}

        {healthData.normal?.length > 0 && (
          <div className="health-section normal">
            <h3>Normal Results</h3>

            {healthData.normal.map((item, index) => (
              <div className="health-card" key={`normal-${index}`}>
                <h4>{item.test}</h4>
                <p>
                  Value: {item.value} {item.unit}
                </p>
                <p>Range: {item.range}</p>
                <strong>Status: {item.status}</strong>
              </div>
            ))}
          </div>
        )}

        {healthData.unverified?.length > 0 && (
          <div className="health-section unverified">
            <h3>Unverified Results</h3>

            {healthData.unverified.map((item, index) => (
              <div className="health-card" key={`unverified-${index}`}>
                <h4>{item.test}</h4>
                <p>Value: {item.value}</p>
                <strong>Status: {item.status}</strong>
              </div>
            ))}
          </div>
        )}
      </>
    );
  };

  return (
    <div className="phone-shell">
      <header className="top-bar">
        <div className="logo-circle">♡</div>

        <div className="brand">
          <h1>HELIO</h1>
          <p>HEALTHCARE AI ASSISTANT</p>
        </div>

        <button
          className={`research-btn ${mode === "research" ? "active" : ""}`}
          onClick={() => setMode(mode === "research" ? "chat" : "research")}
        >
          <span>RESEARCH</span>
          <span>AI</span>
        </button>
      </header>

      <main className="chat-area">
        {messages.length === 0 && (
          <div className="empty-note">
            {mode === "research"
              ? "Search medical papers and PubMed research."
              : "Ask a healthcare question or upload a PDF."}
          </div>
        )}

        {messages.map((msg, index) => (
          <div key={index} className={`msg ${msg.role}`}>
            <span>{msg.role === "user" ? "YOU:" : "AI:"}</span>
            {msg.role === "bot" && msg.healthData?.abnormal?.length > 0 ? (
  <>
    {renderHealthCards(msg.healthData)}
    <p className="safety-note">
      This is a rule-based screening result, not a diagnosis. Please confirm with a qualified doctor.
    </p>
  </>
) : (
  <p>{msg.text}</p>
)}
          </div>
        ))}

        {loading && (
          <div className="msg bot">
            <span>AI:</span>
            <p>Thinking...</p>
          </div>
        )}

        {uploadMessage && <div className="upload-msg">{uploadMessage}</div>}
      </main>

      <footer className="bottom-bar">
        <label className="upload-icon">
          +
          <input
            type="file"
            accept=".pdf"
            onChange={(e) => setFile(e.target.files[0])}
          />
        </label>

        {file && (
          <button className="mini-upload" onClick={uploadPDF}>
            UPLOAD
          </button>
        )}

        <input
          className="main-input"
          type="text"
          placeholder={
            mode === "research" ? "SEARCH RESEARCH..." : "TYPE SOMETHING..."
          }
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
        />

        <button className="send-btn" onClick={sendMessage}>
          ➤
        </button>
      </footer>
    </div>
  );
}