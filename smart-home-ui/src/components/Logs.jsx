import { useEffect, useState } from "react";
import axios from "axios";

const API = "http://localhost:8000";

export default function Logs() {
  const [logs, setLogs] = useState([]);

  const fetchLogs = async () => {
    try {
      const res = await axios.get(`${API}/logs`);
      setLogs(res.data.reverse().slice(0, 50)); // Keep last 50
    } catch (err) {
      console.error("Error fetching logs:", err);
    }
  };

  useEffect(() => {
    fetchLogs();
    const interval = setInterval(fetchLogs, 1000); // Live feel
    return () => clearInterval(interval);
  }, []);

  const formatTime = (ts) => {
    try {
      const date = new Date(ts);
      return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
    } catch {
      return ts;
    }
  };

  return (
    <div className="glass-card">
      <div className="section-title">System Activity</div>
      <div className="log-container">
        {logs.length === 0 ? (
          <div className="log-entry">
            <span className="log-message" style={{ color: 'var(--text-secondary)' }}>
              Initializing system logs...
            </span>
          </div>
        ) : (
          logs.map((log, index) => (
            <div key={index} className="log-entry">
              <span className="log-time">[{formatTime(log.timestamp)}]</span>
              <span className="log-user">{log.user}</span>
              <span className="log-message">→ {log.intent.replace(/_/g, ' ')}</span>
            </div>
          ))
        )}
      </div>
    </div>
  );
}