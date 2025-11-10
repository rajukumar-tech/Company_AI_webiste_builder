// API client for backend services
import { http, normalizeList } from './http';

const api = {
  // Authentication
  login: async (email, password) => {
    const data = await http.post('/api/auth/login', { email, password });
    if (data.token) {
      http.setAuthToken(data.token);
    }
    return data;
  },

  logout: () => {
    http.setAuthToken(null);
  },

  // Services
  getServices: async () => {
    const data = await http.get('/api/pages/services');
    return normalizeList(data.services || []);
  },

  // Projects
  getProjects: async () => {
    const data = await http.get('/api/pages/projects');
    return normalizeList(data.projects || []);
  },

  // Blog Posts
  getPosts: async () => {
    const data = await http.get('/api/blog');
    return normalizeList(data);
  },

  getPost: async (id) => {
    const posts = await api.getPosts();
    return posts.find(post => post.id === id) || null;
  },

  // Jobs & Applications
  getJobs: async () => {
    const data = await http.get('/api/jobs');
    return normalizeList(data);
  },

  submitApplication: async ({ jobId, name, email, phone, skills, coverLetter, resumeFile }) => {
    const formData = new FormData();
    formData.append('name', name);
    formData.append('email', email);
    formData.append('job_title', jobId); // Backend expects job_title
    if (phone) formData.append('phone', phone);
    if (skills) formData.append('desired_skills', skills);
    if (coverLetter) formData.append('cover_letter', coverLetter);
    if (resumeFile) formData.append('resume', resumeFile);

    return http.postFormData('/api/apply', formData);
  },

  // Contact
  sendMessage: async (payload) => {
    return http.post('/api/contact', payload);
  },

  // Admin helpers
  isLoggedIn: () => !!http.getAuthToken()
};

export default api;