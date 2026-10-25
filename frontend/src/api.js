const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export function getToken() {
  return localStorage.getItem('motorstock_token');
}

export function setSession(token, user) {
  localStorage.setItem('motorstock_token', token);
  localStorage.setItem('motorstock_user', JSON.stringify(user));
}

export function clearSession() {
  localStorage.removeItem('motorstock_token');
  localStorage.removeItem('motorstock_user');
}

export function getUser() {
  try {
    return JSON.parse(localStorage.getItem('motorstock_user') || 'null');
  } catch {
    return null;
  }
}

export async function api(path, options = {}) {
  const headers = { 'Content-Type': 'application/json', ...(options.headers || {}) };
  const token = getToken();
  if (token) headers.Authorization = `Bearer ${token}`;

  const response = await fetch(`${API_URL}${path}`, { ...options, headers });
  if (response.status === 401 && token) {
    clearSession();
    window.dispatchEvent(new Event('motorstock:auth-expired'));
  }
  if (response.status === 204) return null;

  const data = await response.json().catch(() => ({}));
  if (!response.ok) {
    throw new Error(data.detail || 'Something went wrong. Please try again.');
  }
  return data;
}
