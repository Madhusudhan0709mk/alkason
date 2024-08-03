import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const setAuthToken = (token) => {
  if (token) {
    api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
  } else {
    delete api.defaults.headers.common['Authorization'];
  }
};

export const stocks = {
  getAll: () => api.get('/stocks'),
  update: (symbol, data) => api.post(`/stocks`, data),
};

export const dataProviders = {
  getAll: () => api.get('/data-providers'),
  update: (name, data) => api.post(`/data-providers`, data),
};

export const brokers = {
  getAll: () => api.get('/brokers'),
  update: (name, data) => api.post(`/brokers`, data),
};

export const aiModels = {
  getAll: () => api.get('/ai-models'),
  update: (name, data) => api.post(`/ai-models`, data),
};

export const tradingStrategies = {
  getAll: () => api.get('/trading-strategies'),
  update: (name, data) => api.post(`/trading-strategies`, data),
};

export const riskManagement = {
  get: () => api.get('/risk-management'),
  update: (data) => api.put('/risk-management', data),
};

export const systemSettings = {
  get: () => api.get('/system-settings'),
  update: (data) => api.put('/system-settings', data),
};

export const decisionEngine = {
  get: () => api.get('/decision-engine-config'),
  update: (data) => api.put('/decision-engine-config', data),
};

export default {
  stocks,
  dataProviders,
  brokers,
  aiModels,
  tradingStrategies,
  riskManagement,
  systemSettings,
  decisionEngine,
};