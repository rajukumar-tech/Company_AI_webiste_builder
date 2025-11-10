import { useEffect } from 'react';
import { Outlet, useNavigate } from 'react-router-dom';
import api from '../lib/api';

export default function AdminLayout() {
  const navigate = useNavigate();

  useEffect(() => {
    if (!api.isLoggedIn()) {
      navigate('/admin/login');
    }
  }, [navigate]);

  const handleLogout = () => {
    api.logout();
    navigate('/admin/login');
  };

  if (!api.isLoggedIn()) {
    return null;
  }

  return (
    <div className="min-h-screen">
      {/* Admin Navigation Header */}
      <nav className="bg-gray-800 text-white px-4 py-3">
        <div className="container mx-auto flex justify-between items-center">
          <div className="text-lg font-semibold">Admin Dashboard</div>
          <button 
            onClick={handleLogout}
            className="btn bg-red-600 hover:bg-red-700 text-white"
          >
            Logout
          </button>
        </div>
      </nav>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        <Outlet />
      </main>
    </div>
  );
}