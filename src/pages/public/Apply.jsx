import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import api from '../../lib/api';

export default function Apply() {
  const { jobId } = useParams();
  const navigate = useNavigate();
  const [job, setJob] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [submitStatus, setSubmitStatus] = useState({ loading: false, error: null, success: false });

  // Form state
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    skills: '',
    coverLetter: '',
    resumeFile: null
  });

  useEffect(() => {
    const loadJob = async () => {
      try {
        const jobs = await api.getJobs();
        const matchingJob = jobs.find(j => j.id === jobId);
        if (matchingJob) {
          setJob(matchingJob);
        } else {
          setError('Job not found');
        }
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    loadJob();
  }, [jobId]);

  const handleChange = (e) => {
    const { name, value, files } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: files ? files[0] : value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitStatus({ loading: true, error: null, success: false });

    try {
      await api.submitApplication({
        jobId: job.id,
        name: formData.name,
        email: formData.email,
        phone: formData.phone,
        skills: formData.skills,
        coverLetter: formData.coverLetter,
        resumeFile: formData.resumeFile
      });
      setSubmitStatus({ loading: false, error: null, success: true });
    } catch (err) {
      setSubmitStatus({ loading: false, error: err.message, success: false });
    }
  };

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
          <h3 className="font-semibold">Error</h3>
          <p>{error}</p>
          <button 
            onClick={() => navigate('/careers')}
            className="btn mt-4"
          >
            Back to Careers
          </button>
        </div>
      </div>
    );
  }

  if (submitStatus.success) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="card p-8 max-w-md w-full text-center">
          <div className="text-green-500 mb-4">
            <svg className="w-16 h-16 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7" />
            </svg>
          </div>
          <h2 className="text-2xl font-bold mb-4">Application Submitted!</h2>
          <p className="text-gray-600 mb-6">
            Thank you for applying. We'll review your application and get back to you soon.
          </p>
          <button 
            onClick={() => navigate('/careers')}
            className="btn"
          >
            Back to Careers
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-12">
      <div className="max-w-2xl mx-auto">
        <button 
          onClick={() => navigate('/careers')}
          className="text-neon mb-8 hover:underline"
        >
          ← Back to Careers
        </button>

        <div className="card p-6 mb-8">
          <h2 className="text-2xl font-bold mb-2">{job.title}</h2>
          {job.skills && (
            <p className="text-gray-600 mb-2">
              <span className="font-medium">Skills:</span> {job.skills}
            </p>
          )}
          <p>{job.description}</p>
        </div>

        <form onSubmit={handleSubmit} className="card p-6">
          <h3 className="text-xl font-semibold mb-6">Apply for this Position</h3>
          
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
              <label className="block text-sm font-medium mb-1">Phone</label>
              <input
                type="tel"
                name="phone"
                className="input w-full"
                value={formData.phone}
                onChange={handleChange}
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">Key Skills</label>
              <input
                type="text"
                name="skills"
                className="input w-full"
                value={formData.skills}
                onChange={handleChange}
                placeholder="e.g., React, Python, Project Management"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">Cover Letter</label>
              <textarea
                name="coverLetter"
                rows="4"
                className="input w-full"
                value={formData.coverLetter}
                onChange={handleChange}
                placeholder="Tell us why you're interested in this position..."
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">Resume (PDF) *</label>
              <input
                type="file"
                name="resumeFile"
                required
                accept=".pdf"
                onChange={handleChange}
                className="input w-full"
              />
            </div>

            {submitStatus.error && (
              <div className="text-red-600 bg-red-50 p-3 rounded">
                {submitStatus.error}
              </div>
            )}

            <button 
              type="submit"
              disabled={submitStatus.loading}
              className="btn w-full"
            >
              {submitStatus.loading ? 'Submitting...' : 'Submit Application'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}