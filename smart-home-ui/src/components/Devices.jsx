import { useEffect, useState } from "react";
import axios from "axios";

const API = "http://localhost:8000";

export default function Devices() {
  const [devices, setDevices] = useState({});

  const fetchDevices = async () => {
    try {
      const res = await axios.get(`${API}/devices`);
      setDevices(res.data);
    } catch (err) {
      console.error("Error fetching devices:", err);
    }
  };

  const toggleDevice = async (device, state) => {
    try {
      await axios.post(`${API}/device-control`, {
        device,
        state,
      });
      fetchDevices();
    } catch (err) {
      console.error("Error toggling device:", err);
    }
  };

  useEffect(() => {
    fetchDevices();
    const interval = setInterval(fetchDevices, 3000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="glass-card">
      <div className="section-title">Device Controls</div>
      {Object.keys(devices).filter(device => device === 'light').map((device) => (
        <div key={device} className={`device-toggle ${devices[device] ? 'active' : ''}`}>
          <div style={{ display: 'flex', flexDirection: 'column' }}>
            <span style={{ fontWeight: '600', textTransform: 'capitalize' }}>
              {device}
            </span>
            <span style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
              Connected • {devices[device] ? 'Running' : 'Standby'}
            </span>
          </div>
          <input
            type="checkbox"
            className="toggle-switch"
            checked={devices[device]}
            onChange={() => toggleDevice(device, !devices[device])}
          />
        </div>
      ))}
    </div>
  );
}