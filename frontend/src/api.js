// Base URL for backend API
const API_BASE = 'http://127.0.0.1:8000';

export async function fetchCompanyData(ticker) {
  const response = await fetch(`${API_BASE}/api/company/${ticker}/`);
  if (!response.ok) throw new Error('Failed to fetch company data');
  return await response.json();
}

export async function uploadFile(file) {
  const formData = new FormData();
  formData.append('file', file);

  const response = await fetch(`${API_BASE}/api/upload/`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) throw new Error('File upload failed');
  return await response.json();
}
