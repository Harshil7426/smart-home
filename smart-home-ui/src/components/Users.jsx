import { useEffect, useState } from "react";
import axios from "axios";

const API = "https://smart-home-4b7r.onrender.com/";

export default function Users() {
  const [users, setUsers] = useState({});

  const fetchUsers = async () => {
    const res = await axios.get(`${API}/users`);
    setUsers(res.data);
  };

  useEffect(() => {
    fetchUsers();
  }, []);

  return (
    <div style={{ marginBottom: "30px" }}>
      <h2>Users</h2>
      {Object.keys(users).map((username) => (
        <div key={username}>
          {username} — Light:{" "}
          {users[username].default_light ? "ON" : "OFF"} | Fan:{" "}
          {users[username].default_fan ? "ON" : "OFF"}
        </div>
      ))}
    </div>
  );
}