import Devices from "./Devices";
import Logs from "./Logs";
import Users from "./Users";

export default function Dashboard() {
  return (
    <div style={{ padding: "20px", fontFamily: "Arial" }}>
      <h1>Smart Home Dashboard</h1>
      <Devices />
      <Users />
      <Logs />
    </div>
  );
}