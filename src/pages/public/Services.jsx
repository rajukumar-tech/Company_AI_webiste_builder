import { useState, useEffect } from 'react';
import api from '../../lib/api';

export default function Services() {
  const [services, setServices] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const loadServices = async () => {
      try {
        const data = await api.getServices();
        setServices(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    loadServices();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-16 w-16 border-t-2 border-b-2 border-neon"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="card bg-red-50 p-6 text-red-800">
          <h3 className="font-semibold">Error Loading Services</h3>
          <p>{error}</p>
        </div>
      </div>
    );
  }

  if (!services.length) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="card p-6">
          <h3 className="text-xl">No services yet.</h3>
          <p className="text-gray-600 mt-2">Check back soon for our offerings.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-12">
      <h1 className="section-title text-4xl font-bold text-center mb-12">Our Services</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        {services.map((service, index) => (
          <div key={index} className="card p-6 hover:shadow-lg transition-shadow duration-300">
            <h3 className="text-xl font-semibold mb-3">{service}</h3>
            <p className="text-gray-600">{service.description}</p>
          </div>
        ))}
      </div>
    </div>
  );
}