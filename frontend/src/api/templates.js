/**
 * Templates feature API: list contract templates.
 */
import { API_BASE_URL, handleResponse } from "./common.js";

export async function fetchTemplates(token) {
  const response = await fetch(`${API_BASE_URL}/api/templates`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return handleResponse(response);
}

export async function fetchTemplateContent(templateName, token) {
  const response = await fetch(`${API_BASE_URL}/api/templates/${templateName}/content`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return handleResponse(response);
}
