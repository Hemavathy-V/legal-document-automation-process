/**
 * Login page: email + password form, submits to /api/login.
 */
import React, { useState } from "react";
import { login } from "../../api/login.js";

const LAST_EMAIL_KEY = "lca_last_email";

function LoginPage({ onLoginSuccess }) {
  const [email, setEmail] = useState(
    () => localStorage.getItem(LAST_EMAIL_KEY) ?? ""
  );
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const result = await login(email, password);
      localStorage.setItem(LAST_EMAIL_KEY, email);
      onLoginSuccess(result);
    } catch (err) {
      setError(err.message || "Login failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <form className="form login-form" onSubmit={handleSubmit}>
      <h2>Login</h2>
      <label className="field">
        <span>Email</span>
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value.toLowerCase())}
          placeholder="you@example.com"
          required
        />
      </label>
      <label className="field">
        <span>Password</span>
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Your password"
          required
        />
      </label>
      <button type="submit" disabled={loading}>
        {loading ? "Logging in..." : "Login"}
      </button>
      {error && <p className="error">{error}</p>}
    </form>
  );
}

export default LoginPage;
