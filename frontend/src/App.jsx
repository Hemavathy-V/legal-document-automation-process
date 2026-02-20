/**
 * App shell: shows Login page or (user info + dashboard pages).
 */
import React, { useState } from "react";
import LoginPage from "./pages/login/LoginPage.jsx";
import ContractGenerationPage from "./pages/ContractGenerationPage.jsx";
import ContractsPage from "./pages/contracts/ContractsPage.jsx";
import TemplatesPage from "./pages/templates/TemplatesPage.jsx";

function App() {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState("");
  const [activePage, setActivePage] = useState("generate");

  const handleLoginSuccess = (result) => {
    setUser(result.user);
    setToken(result.access_token);
  };

  const handleLogout = () => {
    setUser(null);
    setToken("");
    setActivePage("generate");
  };

  return (
    <div className="app-container">
      <div className={`card ${!user ? "card--login" : ""}`}>
        <h1>Legal Contract Management</h1>

        {!user && <LoginPage onLoginSuccess={handleLoginSuccess} />}

        {user && (
          <>
            <div className="user-info">
              <div>
                <strong>Logged in as:</strong> {user.user_name} ({user.email})
              </div>
              <div>
                <strong>Role:</strong> {user.role}
              </div>
              <button onClick={handleLogout} className="btn btn-secondary" style={{ marginTop: '0.5rem' }}>
                Logout
              </button>
            </div>

            {/* Navigation */}
            <div className="tabs">
              <button
                className={`tab-btn ${activePage === "generate" ? "tab-active" : ""}`}
                onClick={() => setActivePage("generate")}
              >
                Generate Contract
              </button>
              <button
                className={`tab-btn ${activePage === "contracts" ? "tab-active" : ""}`}
                onClick={() => setActivePage("contracts")}
              >
                My Contracts
              </button>
              <button
                className={`tab-btn ${activePage === "templates" ? "tab-active" : ""}`}
                onClick={() => setActivePage("templates")}
              >
                Templates
              </button>
            </div>

            {/* Pages */}
            {activePage === "generate" && <ContractGenerationPage />}
            {activePage === "contracts" && <ContractsPage token={token} />}
            {activePage === "templates" && <TemplatesPage token={token} />}
          </>
        )}
      </div>
    </div>
  );
}

export default App;
