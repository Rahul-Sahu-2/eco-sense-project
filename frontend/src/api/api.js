import axios from 'axios';

const API_BASE = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE,
  timeout: 60000,
});

// Attach token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// ── Auth ──
export const loginUser = (data) => api.post('/api/auth/login', data);
export const registerUser = (data) => api.post('/api/auth/register', data);

// ── Detection ──
export const detectWaste = (imageBase64, confidence = 0.1) =>
  api.post('/api/detect', { image: imageBase64, confidence });

export const getDetectionTip = (items) =>
  api.post('/api/detect/tip', { items });

export const getDetectionExplanation = (items) =>
  api.post('/api/detect/explain', { items });

// ── Chatbot ──
export const sendChatMessage = (message) =>
  api.post('/api/chat', { message });

// ── Citizen ──
export const analyzeCitizenImage = (file) => {
  const formData = new FormData();
  formData.append('file', file);
  return api.post('/api/citizen/analyze', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
};

export const submitCitizenReport = (data) =>
  api.post('/api/citizen/report', data);

export const getCitizenConfig = () =>
  api.get('/api/citizen/config');

// ── Blockchain ──
export const verifyBlockchainImage = (file) => {
  const formData = new FormData();
  formData.append('file', file);
  return api.post('/api/blockchain/verify', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
};

export const claimBlockchainReward = (wallet, tokens) =>
  api.post('/api/blockchain/reward', { wallet, tokens });

// ── Admin ──
export const getAdminReports = () =>
  api.get('/api/admin/reports');

export const getAdminStats = () =>
  api.get('/api/admin/stats');

export const downloadReportsCSV = () =>
  `${API_BASE}/api/admin/reports/download`;

export default api;
