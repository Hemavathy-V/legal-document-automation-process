// Use same origin so Vite dev server can proxy /api and /health to the backend
const API_BASE_URL = "";

async function handleResponse(response) {
  if (!response.ok) {
    let message = "Request failed";
    try {
      const data = await response.json();
      if (data && data.detail) {
        if (typeof data.detail === "string") {
          message = data.detail;
        } else if (Array.isArray(data.detail)) {
          // Pydantic validation errors — pick the first human-readable message
          message = data.detail.map((e) => e.msg).join("; ");
        }
      }
    } catch {
      // ignore JSON parse failures
    }
    throw new Error(message);
  }
  return response.json();
}

export { API_BASE_URL, handleResponse };
