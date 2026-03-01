import { useEffect, useState } from "react";
import axios from "axios";

const API = "https://smart-home-4b7r.onrender.com/";

export default function Logs() {
  const [logs, setLogs] = useState([]);

  const fetchLogs = async () => {
    const res = await axios.get(`${API}/logs`);
    setLogs(res.data.reverse());
  };

  useEffect(() => {
    fetchLogs();
    const interval = setInterval(fetchLogs, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div>
      <h2>Activity Logs</h2>
      {logs.map((log, index) => (
        <div key={index} style={{ marginBottom: "5px" }}>
          {log.timestamp} — {log.user} → {log.intent}
        </div>
      ))}
    </div>
  );
}