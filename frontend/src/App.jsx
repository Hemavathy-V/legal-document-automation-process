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
import ContractGenerationPage from "./pages/ContractGenerationPage.jsx";
import ContractsPage from "./pages/contracts/ContractsPage.jsx";
import TemplatesPage from "./pages/templates/TemplatesPage.jsx";
import UsersPage from "./pages/admin/UsersPage.jsx";

const ROLE_TABS = {
  Admin: ["contracts", "generate", "templates", "users"],
  Lawyer: ["contracts", "generate", "templates"],
  "Assistant Lawyer": ["contracts", "generate", "templates"],
  Client: ["contracts"],
};

const TAB_LABELS = {
  contracts: "Contracts",
  generate: "Generate",
  templates: "Templates",
  users: "Users",
};

const SESSION_KEY = "lca_session";

function loadSession() {
  try {
    const raw = localStorage.getItem(SESSION_KEY);
    if (!raw) return null;
    return JSON.parse(raw);
  } catch {
    return null;
  }
}

function App() {
  const saved = loadSession();
  const [user, setUser] = useState(saved?.user ?? null);
  const [token, setToken] = useState(saved?.token ?? "");
  const [activeTab, setActiveTab] = useState("contracts");

  const handleLoginSuccess = (result) => {
    setUser(result.user);
    setToken(result.access_token);
    setActiveTab("contracts");
    localStorage.setItem(
      SESSION_KEY,
      JSON.stringify({ user: result.user, token: result.access_token })
    );
  };

  const handleLogout = () => {
    setUser(null);
    setToken("");
    setActiveTab("contracts");
    localStorage.removeItem(SESSION_KEY);
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
        {activeTab === "generate" && <ContractGenerationPage token={token} />}
        {activeTab === "templates" && <TemplatesPage token={token} />}
        {activeTab === "users" && user.role === "Admin" && (
          <UsersPage token={token} currentUserId={user.user_id} />
        )}
      </main>
    </div>
  );
}

export default App;
