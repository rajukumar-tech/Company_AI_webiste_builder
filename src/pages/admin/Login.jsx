import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../../lib/api';

// Whitelist of allowed admin emails
const ADMIN_WHITELIST = ["admin1@yourdomain.com", "admin2@yourdomain.com"];

export default function Login() {
  const navigate = useNavigate();
  const [credentials, setCredentials] = useState({ email: '', password: '' });
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setCredentials(prev => ({
      ...prev,
      [name]: value
    }));
    setError(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    // Check whitelist
    if (!ADMIN_WHITELIST.includes(credentials.email)) {
      setError('Access denied. Not authorized.');
      setLoading(false);
      return;
    }

    try {
      await api.login(credentials.email, credentials.password);
      navigate('/admin/dashboard');
    } catch (err) {
      setError('Invalid credentials');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="max-w-md w-full">
        <h1 className="text-3xl font-bold text-center mb-8">Admin Login</h1>

        <form onSubmit={handleSubmit} className="card p-6">
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-1">Email</label>
              <input
                type="email"
                name="email"
                required
                className="input w-full"
                value={credentials.email}
                onChange={handleChange}
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">Password</label>
              <input
                type="password"
                name="password"
                required
                className="input w-full"
                value={credentials.password}
                onChange={handleChange}
              />
            </div>

            {error && (
              <div className="text-red-600 bg-red-50 p-3 rounded">
                {error}
              </div>
            )}

            <button 
              type="submit"
              disabled={loading}
              className="btn w-full"
            >
              {loading ? 'Logging in...' : 'Log In'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}