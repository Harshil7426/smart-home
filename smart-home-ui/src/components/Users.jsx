import { useEffect, useState } from "react";
import axios from "axios";

const API = "http://localhost:8000";

export default function Users() {
  const [users, setUsers] = useState({});

  const fetchUsers = async () => {
    try {
      const res = await axios.get(`${API}/users`);
      setUsers(res.data);
    } catch (err) {
      console.error("Error fetching users:", err);
    }
  };

  useEffect(() => {
    fetchUsers();
  }, []);

  return (
    <div className="glass-card">
      <div className="section-title">Authorized Residents</div>
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px' }}>
        {Object.keys(users).map((username) => (
          <div key={username} style={{
            background: 'rgba(255, 255, 255, 0.03)',
            padding: '16px',
            borderRadius: '12px',
            border: '1px solid var(--glass-border)'
          }}>
            <div style={{ fontWeight: '700', fontSize: '1.1rem', marginBottom: '8px', color: 'var(--accent-cyan)' }}>
              {username}
            </div>
            <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', display: 'flex', flexDirection: 'column', gap: '4px' }}>
              <span>Light Pref: <strong style={{ color: '#fff' }}>{users[username].default_light ? "ON" : "OFF"}</strong></span>
              <span>Fan Pref: <strong style={{ color: '#fff' }}>{users[username].default_fan ? "ON" : "OFF"}</strong></span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}