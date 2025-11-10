// HTTP adapter with token auth and response normalization
const BASE_URL = import.meta.env.VITE_API_BASE_URL?.replace(/\/$/, '') || 'http://localhost:5001';

// Normalize list responses to handle different backend formats
const normalizeList = (data) => {
  if (Array.isArray(data)) return data;
  if (data?.data) return data.data;
  if (data?.items) return data.items;
  if (data?.result) return data.result;
  return [];
};

const http = {
  getAuthToken: () => localStorage.getItem('auth_token'),

  setAuthToken: (token) => {
    if (token) {
      localStorage.setItem('auth_token', token);
    } else {
      localStorage.removeItem('auth_token');
    }
  },

  request: async (endpoint, options = {}) => {
    const url = `${BASE_URL}${endpoint}`;
    const headers = {
      'Accept': 'application/json',
      ...options.headers
    };

    // Add auth token if present
    const token = http.getAuthToken();
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    // Handle FormData vs JSON
    if (!(options.body instanceof FormData)) {
      headers['Content-Type'] = 'application/json';
      if (options.body) {
        options.body = JSON.stringify(options.body);
      }
    }

    try {
      const response = await fetch(url, {
        ...options,
        headers
      });

      // Handle non-JSON responses (like application/octet-stream)
      const contentType = response.headers.get('content-type');
      const data = contentType?.includes('application/json') 
        ? await response.json()
        : await response.text();

      if (!response.ok) {
        throw new Error(data.error || 'Network response was not ok');
      }

      return data;
    } catch (error) {
      // Check for CORS error
      if (error.message.includes('CORS')) {
        throw new Error('CORS error: Unable to connect to backend server. Please ensure the backend is running and CORS is enabled.');
      }
      throw error;
    }
  },

  get: (endpoint) => http.request(endpoint, { method: 'GET' }),
  
  post: (endpoint, data) => http.request(endpoint, {
    method: 'POST',
    body: data
  }),

  postFormData: (endpoint, formData) => http.request(endpoint, {
    method: 'POST',
    body: formData
  })
};

export { http, normalizeList };