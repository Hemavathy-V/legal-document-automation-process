/**
 * Users feature API: list users, create user, update user, delete user.
 */
import { API_BASE_URL, handleResponse } from "./common.js";

export async function fetchUsers(token) {
  const response = await fetch(`${API_BASE_URL}/api/users`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return handleResponse(response);
}

export async function createUser({ user_name, email, password, role }, token) {
  const response = await fetch(`${API_BASE_URL}/api/register`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ user_name, email, password, role }),
  });
  return handleResponse(response);
}

export async function updateUser(userId, { user_name, email, password, role }, token) {
  const body = { user_name, email, role };
  if (password && password.trim()) body.password = password.trim();
  const response = await fetch(`${API_BASE_URL}/api/users/${userId}`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify(body),
  });
  return handleResponse(response);
}

export async function deleteUser(userId, token) {
  const response = await fetch(`${API_BASE_URL}/api/users/${userId}`, {
    method: "DELETE",
    headers: { Authorization: `Bearer ${token}` },
  });
  if (response.status === 204) return;
  return handleResponse(response);
}
