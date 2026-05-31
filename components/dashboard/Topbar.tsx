export default function Topbar() {
  const role = localStorage.getItem("role");

  return (
    <div className="topbar">
      <div>
        <h1>Admin Dashboard</h1>
        <p>Realtime MBBS Study Analytics</p>
      </div>

      <div className="user-badge">
        <span>{role}</span>
      </div>
    </div>
  );
}