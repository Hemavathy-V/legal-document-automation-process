/**
 * App shell: login gate + role-based dashboard with tab navigation.
 *
 * Role → visible tabs
 *   Admin            : Contracts | Templates | Users
 *   Lawyer           : Contracts | Templates
 *   Assistant Lawyer : Contracts | Templates
 *   Client           : Contracts
 */
import React, { useState } from "react";
import LoginPage from "./pages/login/LoginPage.jsx";
import ContractsPage from "./pages/contracts/ContractsPage.jsx";
import TemplatesPage from "./pages/templates/TemplatesPage.jsx";
import UsersPage from "./pages/admin/UsersPage.jsx";

const ROLE_TABS = {
  Admin: ["contracts", "templates", "users"],
  Lawyer: ["contracts", "templates"],
  "Assistant Lawyer": ["contracts", "templates"],
  Client: ["contracts"],
};

const TAB_LABELS = {
  contracts: "Contracts",
  templates: "Templates",
  users: "Users",
};

function App() {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState("");
  const [activeTab, setActiveTab] = useState("contracts");

  const handleLoginSuccess = (result) => {
    setUser(result.user);
    setToken(result.access_token);
    setActiveTab("contracts");
  };

  const handleLogout = () => {
    setUser(null);
    setToken("");
    setActiveTab("contracts");
  };

  if (!user) {
    return (
      <div className="app-container">
        <div className="card card--login">
          <h1>Legal Contract Management</h1>
          <LoginPage onLoginSuccess={handleLoginSuccess} />
        </div>
      </div>
    );
  }

  const tabs = ROLE_TABS[user.role] ?? ["contracts"];

  return (
    <div className="dashboard">
      {/* ── Top navigation bar ── */}
      <header className="top-nav">
        <span className="nav-brand">Legal Contract Management</span>
        <div className="nav-user">
          <span className="nav-user-name">{user.user_name}</span>
          <span className={`role-badge role-badge--${user.role.toLowerCase().replace(/\s+/g, "-")}`}>
            {user.role}
          </span>
          <button className="btn-logout" onClick={handleLogout}>
            Logout
          </button>
        </div>
      </header>

      {/* ── Tab navigation ── */}
      <nav className="tab-nav">
        {tabs.map((tab) => (
          <button
            key={tab}
            className={`tab-btn${activeTab === tab ? " tab-btn--active" : ""}`}
            onClick={() => setActiveTab(tab)}
          >
            {TAB_LABELS[tab]}
          </button>
        ))}
      </nav>

      {/* ── Page content ── */}
      <main className="dashboard-content">
        {activeTab === "contracts" && <ContractsPage token={token} />}
        {activeTab === "templates" && <TemplatesPage token={token} />}
        {activeTab === "users" && user.role === "Admin" && (
          <UsersPage token={token} currentUserId={user.user_id} />
        )}
      </main>
    </div>
  );
}

export default App;
