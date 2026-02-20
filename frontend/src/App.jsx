/**
 * App shell: shows Login page or (user info + Contracts + Templates pages).
 */
import React, { useState } from "react";
import LoginPage from "./pages/login/LoginPage.jsx";
import ContractsPage from "./pages/contracts/ContractsPage.jsx";
import TemplatesPage from "./pages/templates/TemplatesPage.jsx";

function App() {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState("");

  const handleLoginSuccess = (result) => {
    setUser(result.user);
    setToken(result.access_token);
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
            </div>

            <ContractsPage token={token} />
            <TemplatesPage token={token} />
          </>
        )}
      </div>
    </div>
  );
}

export default App;
