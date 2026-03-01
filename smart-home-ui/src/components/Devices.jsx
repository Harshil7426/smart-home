import { useEffect, useState } from "react";
import axios from "axios";

const API = "https://smart-home-4b7r.onrender.com";

export default function Devices() {
  const [devices, setDevices] = useState({});

  const fetchDevices = async () => {
    const res = await axios.get(`${API}/devices`);
    setDevices(res.data);
  };

  const toggleDevice = async (device, state) => {
    await axios.post(`${API}/device-control`, {
      device,
      state,
    });
    fetchDevices();
  };

  useEffect(() => {
    fetchDevices();
    const interval = setInterval(fetchDevices, 3000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div style={{ marginBottom: "30px" }}>
      <h2>Devices</h2>
      {Object.keys(devices).map((device) => (
        <div key={device}>
          <strong>{device.toUpperCase()}</strong> :{" "}
          {devices[device] ? "ON" : "OFF"}
          <button
            onClick={() => toggleDevice(device, !devices[device])}
            style={{ marginLeft: "10px" }}
          >
            Toggle
          </button>
        </div>
      ))}
    </div>
  );
}