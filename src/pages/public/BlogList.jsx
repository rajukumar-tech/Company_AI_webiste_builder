import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from '../../lib/api';

export default function BlogList() {
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const loadPosts = async () => {
      try {
        const data = await api.getPosts();
        setPosts(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    loadPosts();
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
          <h3 className="font-semibold">Error Loading Blog Posts</h3>
          <p>{error}</p>
        </div>
      </div>
    );
  }

  if (!posts.length) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="card p-6">
          <h3 className="text-xl">No blog posts yet.</h3>
          <p className="text-gray-600 mt-2">Check back soon for new content.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-12">
      <h1 className="section-title text-4xl font-bold text-center mb-12">Blog</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        {posts.map(post => (
          <Link 
            key={post.id} 
            to={`/blog/${post.id}`}
            className="card p-6 hover:shadow-lg transition-shadow duration-300"
          >
            <h2 className="text-xl font-semibold mb-3">{post.title}</h2>
            <p className="text-gray-600 line-clamp-3">{post.summary || post.content}</p>
            <div className="mt-4 text-neon">Read more →</div>
          </Link>
        ))}
      </div>
    </div>
  );
}