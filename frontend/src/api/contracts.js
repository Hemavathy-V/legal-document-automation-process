/**
 * Contracts feature API: list contracts, fetch placeholders, and generate contracts.
 */
import { API_BASE_URL, handleResponse } from "./common.js";

export async function fetchContracts(token) {
  const response = await fetch(`${API_BASE_URL}/api/contracts`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return handleResponse(response);
}

export async function fetchTemplates() {
  const response = await fetch(`${API_BASE_URL}/templates`);
  return handleResponse(response);
}

export async function fetchPlaceholders(templateName) {
  const response = await fetch(`${API_BASE_URL}/templates/${templateName}/placeholders`);
  return handleResponse(response);
}

export async function submitContract(templateName, data) {
  const response = await fetch(`${API_BASE_URL}/contracts/data`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ template_name: templateName, data }),
  });
  return handleResponse(response);
}
