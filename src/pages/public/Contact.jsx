import { useState } from 'react';
import api from '../../lib/api';

export default function Contact() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    message: ''
  });
  const [status, setStatus] = useState({ loading: false, error: null, success: false });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setStatus({ loading: true, error: null, success: false });

    try {
      await api.sendMessage(formData);
      setStatus({ loading: false, error: null, success: true });
      setFormData({ name: '', email: '', message: '' });
    } catch (err) {
      setStatus({ loading: false, error: err.message, success: false });
    }
  };

  if (status.success) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="card p-8 max-w-md w-full text-center">
          <div className="text-green-500 mb-4">
            <svg className="w-16 h-16 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7" />
            </svg>
          </div>
          <h2 className="text-2xl font-bold mb-4">Message Sent!</h2>
          <p className="text-gray-600 mb-6">
            Thank you for contacting us. We'll get back to you soon.
          </p>
          <button 
            onClick={() => setStatus({ loading: false, error: null, success: false })}
            className="btn"
          >
            Send Another Message
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-12">
      <div className="max-w-2xl mx-auto">
        <h1 className="section-title text-4xl font-bold text-center mb-12">Contact Us</h1>

        <form onSubmit={handleSubmit} className="card p-6">
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-1">Name *</label>
              <input
                type="text"
                name="name"
                required
                className="input w-full"
                value={formData.name}
                onChange={handleChange}
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">Email *</label>
              <input
                type="email"
                name="email"
                required
                className="input w-full"
                value={formData.email}
                onChange={handleChange}
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">Message *</label>
              <textarea
                name="message"
                required
                rows="6"
                className="input w-full"
                value={formData.message}
                onChange={handleChange}
              />
            </div>

            {status.error && (
              <div className="text-red-600 bg-red-50 p-3 rounded">
                {status.error}
              </div>
            )}

            <button 
              type="submit"
              disabled={status.loading}
              className="btn w-full"
            >
              {status.loading ? 'Sending...' : 'Send Message'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}