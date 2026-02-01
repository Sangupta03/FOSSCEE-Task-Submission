const BASE = process.env.REACT_APP_API_BASE;

const USER = process.env.REACT_APP_API_USER;
const PASS = process.env.REACT_APP_API_PASS;

const AUTH_HEADER = "Basic " + btoa(`${USER}:${PASS}`);

async function request(url, options = {}) {
  const res = await fetch(url, {
    ...options,
    headers: {
      ...(options.headers || {}),
      Authorization: AUTH_HEADER,
    },
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export function getSummary() {
  return request(`${BASE}/summary/`);
}

export function getHistory() {
  return request(`${BASE}/history/`);
}

export async function uploadCSV(file) {
  const form = new FormData();
  form.append("file", file);

  const res = await fetch(`${BASE}/upload/`, {
    method: "POST",
    body: form,
    headers: {
      Authorization: AUTH_HEADER,
    },
  });

  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

