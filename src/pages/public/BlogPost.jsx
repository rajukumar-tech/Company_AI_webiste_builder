import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import api from '../../lib/api';

export default function BlogPost() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [post, setPost] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const loadPost = async () => {
      try {
        const data = await api.getPost(id);
        if (data) {
          setPost(data);
        } else {
          setError('Post not found');
        }
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    loadPost();
  }, [id]);

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
          <h3 className="font-semibold">Error Loading Post</h3>
          <p>{error}</p>
          <button 
            onClick={() => navigate('/blog')}
            className="btn mt-4"
          >
            Back to Blog
          </button>
        </div>
      </div>
    );
  }

  if (!post) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="card p-6">
          <h3 className="text-xl">Post not found</h3>
          <button 
            onClick={() => navigate('/blog')}
            className="btn mt-4"
          >
            Back to Blog
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-12">
      <article className="max-w-4xl mx-auto">
        <button 
          onClick={() => navigate('/blog')}
          className="text-neon mb-8 hover:underline"
        >
          ← Back to Blog
        </button>

        <h1 className="text-4xl font-bold mb-6">{post.title}</h1>
        
        <div className="prose max-w-none">
          {post.content.split('\n').map((paragraph, idx) => (
            <p key={idx} className="mb-4">{paragraph}</p>
          ))}
        </div>
      </article>
    </div>
  );
}