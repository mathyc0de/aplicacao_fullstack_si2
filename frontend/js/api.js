async function apiGet(path, params = {}) {
  const url = new URL(path, window.location.origin);
  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== null && String(value).trim() !== "") {
      url.searchParams.set(key, value);
    }
  });
  const response = await fetch(url.toString(), {
    headers: { Accept: "application/json" },
  });
  const payload = await response.json().catch(() => ({}));
  if (!response.ok) {
    const error = new Error(payload.message || "Falha ao consultar a API.");
    error.payload = payload;
    error.status = response.status;
    throw error;
  }
  return payload;
}

function searchServidores(params) {
  return apiGet(`${AppConfig.apiBase}/servidores`, params);
}

function fetchCargos() {
  return apiGet(`${AppConfig.apiBase}/cargos`);
}

function fetchOrgaos() {
  return apiGet(`${AppConfig.apiBase}/orgaos`);
}

function fetchUfs() {
  return apiGet(`${AppConfig.apiBase}/ufs`);
}
