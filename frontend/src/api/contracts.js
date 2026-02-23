/**
 * Contracts feature API: list contracts.
 */
import { API_BASE_URL, handleResponse } from "./common.js";

export async function fetchContracts(token) {
  const response = await fetch(`${API_BASE_URL}/api/contracts`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return handleResponse(response);
}
