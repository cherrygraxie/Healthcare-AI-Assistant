import { useState } from "react";
import axios from "axios";
import "./Chat.css";

export default function Chat() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const question = input;

    const userMessage = {
      role: "user",
      text: question,
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setLoading(true);

    try {
      const res = await axios.get(
        `http://127.0.0.1:8000/ask?question=${encodeURIComponent(question)}`
      );

      const botMessage = {
        role: "bot",
        text: res.data.answer,
      };

      setMessages((prev) => [...prev, botMessage]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        {
          role: "bot",
          text: "Unable to connect to backend.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter") {
      sendMessage();
    }
  };

  return (
    <div className="chat-container">
      <div className="chat-header">
        Healthcare AI Assistant
      </div>

      <div className="chat-window">
        {messages.length === 0 && (
          <div className="welcome-message">
            Ask a healthcare-related question to begin.
          </div>
        )}

        {messages.map((msg, index) => (
          <div
            key={index}
            className={`message ${msg.role}`}
          >
            <div className="bubble">
              {msg.text}
            </div>
          </div>
        ))}

        {loading && (
          <div className="message bot">
            <div className="bubble">
              AI is thinking...
            </div>
          </div>
        )}
      </div>

      <div className="input-area">
        <input
          type="text"
          placeholder="Ask anything..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyPress}
        />

        <button onClick={sendMessage}>
          Send
        </button>
      </div>
    </div>
  );
}