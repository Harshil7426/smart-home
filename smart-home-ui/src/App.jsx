import Devices from "./components/Devices";
import Logs from "./components/Logs";
import LiveFeed from "./components/LiveFeed";

export default function App() {
  return (
    <div className="dashboard-container">
      <h1>Home OS <span style={{ color: 'var(--accent-cyan)', fontSize: '1rem', fontWeight: '400' }}>v2.0.4 - ACTIVE</span></h1>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
        <LiveFeed />
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
        <Devices />
        <Logs />
      </div>
    </div>
  );
}