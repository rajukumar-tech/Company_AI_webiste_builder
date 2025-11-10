import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from '../../lib/api';

export default function Careers() {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const loadJobs = async () => {
      try {
        const data = await api.getJobs();
        setJobs(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    loadJobs();
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
          <h3 className="font-semibold">Error Loading Job Listings</h3>
          <p>{error}</p>
        </div>
      </div>
    );
  }

  if (!jobs.length) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="card p-6">
          <h3 className="text-xl">No open positions at the moment</h3>
          <p className="text-gray-600 mt-2">Check back soon for new opportunities.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-12">
      <h1 className="section-title text-4xl font-bold text-center mb-12">We're Hiring</h1>
      
      <div className="grid grid-cols-1 gap-8 max-w-4xl mx-auto">
        {jobs.map(job => (
          <div key={job.id} className="card p-6">
            <div className="flex justify-between items-start">
              <div>
                <h2 className="text-2xl font-semibold mb-2">{job.title}</h2>
                <div className="text-gray-600 mb-4">
                  {job.skills && (
                    <p className="mb-2">
                      <span className="font-medium">Skills:</span> {job.skills}
                    </p>
                  )}
                </div>
                <p className="mb-4">{job.description}</p>
              </div>
              <Link 
                to={`/apply/${job.id}`}
                className="btn hover:shadow-lg transition-shadow duration-300"
              >
                Apply →
              </Link>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}