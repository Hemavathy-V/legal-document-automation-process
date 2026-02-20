// Use same origin so Vite dev server can proxy /api and /health to the backend
const API_BASE_URL = "";

async function handleResponse(response) {
  if (!response.ok) {
    let message = "Request failed";
    try {
      const data = await response.json();
      if (data && data.detail) message = data.detail;
    } catch {
      // ignore
    }
    throw new Error(message);
  }
  return response.json();
}

export { API_BASE_URL, handleResponse };
