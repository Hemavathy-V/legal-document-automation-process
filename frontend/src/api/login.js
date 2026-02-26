/**
 * Login feature API: login and register.
 */
import { API_BASE_URL, handleResponse } from "./common.js";

export async function login(email, password) {
  const response = await fetch(`${API_BASE_URL}/api/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });
  return handleResponse(response);
}

export async function register({ user_name, email, password, role }) {
  const response = await fetch(`${API_BASE_URL}/api/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ user_name, email, password, role }),
  });
  return handleResponse(response);
}
