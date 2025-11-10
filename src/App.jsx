import { Routes, Route, Navigate } from 'react-router-dom';
import SiteLayout from './layouts/SiteLayout';
import AdminLayout from './layouts/AdminLayout';

// Public pages
import Home from './pages/public/Home';
import About from './pages/public/About';
import Services from './pages/public/Services';
import Projects from './pages/public/Projects';
import BlogList from './pages/public/BlogList';
import BlogPost from './pages/public/BlogPost';
import Contact from './pages/public/Contact';
import Careers from './pages/public/Careers';
import Apply from './pages/public/Apply';

// Admin pages
import Login from './pages/admin/Login';
import Dashboard from './pages/admin/Dashboard';
import Posts from './pages/admin/Posts';
import Jobs from './pages/admin/Jobs';
import Applications from './pages/admin/Applications';
import Messages from './pages/admin/Messages';

export default function App() {
  return (
    <Routes>
      {/* Public Routes */}
      <Route path="/" element={<SiteLayout />}>
        <Route index element={<Home />} />
        <Route path="about" element={<About />} />
        <Route path="services" element={<Services />} />
        <Route path="projects" element={<Projects />} />
        <Route path="blog" element={<BlogList />} />
        <Route path="blog/:id" element={<BlogPost />} />
        <Route path="contact" element={<Contact />} />
        <Route path="careers" element={<Careers />} />
        <Route path="apply/:jobId" element={<Apply />} />
      </Route>

      {/* Admin Routes */}
      <Route path="/admin" element={<AdminLayout />}>
        <Route index element={<Navigate to="/admin/dashboard" replace />} />
        <Route path="login" element={<Login />} />
        <Route path="dashboard" element={<Dashboard />} />
        <Route path="posts" element={<Posts />} />
        <Route path="jobs" element={<Jobs />} />
        <Route path="applications" element={<Applications />} />
        <Route path="messages" element={<Messages />} />
      </Route>
    </Routes>
  );
}