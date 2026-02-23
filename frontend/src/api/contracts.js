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

export async function fetchTemplates(token) {
  const response = await fetch(`${API_BASE_URL}/api/templates`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return handleResponse(response);
}

export async function fetchPlaceholders(templateName, token) {
  const response = await fetch(`${API_BASE_URL}/api/templates/${templateName}/placeholders`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return handleResponse(response);
}

export async function submitContract(templateName, data, token) {
  const response = await fetch(`${API_BASE_URL}/api/contracts/data`, {
    method: "POST",
    headers: { 
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ template_name: templateName, data }),
  });
  return handleResponse(response);
}
