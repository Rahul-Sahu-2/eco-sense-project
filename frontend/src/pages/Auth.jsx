import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { loginUser, registerUser } from '../api/api';

export default function Auth() {
  const [isLogin, setIsLogin] = useState(true);
  const [formData, setFormData] = useState({ username: '', email: '', password: '' });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      if (isLogin) {
        const res = await loginUser({ username: formData.username, password: formData.password });
        localStorage.setItem('token', res.data.access_token);
        localStorage.setItem('user', formData.username);
        navigate('/admin');
      } else {
        await registerUser(formData);
        setIsLogin(true);
        setError('Registration successful! Please login.');
      }
    } catch (err) {
      setError(err.response?.data?.detail || 'Something went wrong');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-container fade-in">
      <div className="glass-card auth-card">
        <div className="auth-header">
          <div className="logo-box" style={{ margin: '0 auto 1.5rem' }}>🛰️</div>
          <h2>{isLogin ? 'Welcome Back' : 'Create Account'}</h2>
          <p>{isLogin ? 'Sign in to access the monitor' : 'Join the EcoSense initiative'}</p>
        </div>

        {error && <div className={`auth-alert ${error.includes('successful') ? 'success' : ''}`}>{error}</div>}

        <form onSubmit={handleSubmit} className="auth-form">
          <div className="form-group">
            <label>Username</label>
            <input 
              type="text" 
              required 
              value={formData.username}
              onChange={(e) => setFormData({...formData, username: e.target.value})}
              placeholder="Enter your username"
            />
          </div>

          {!isLogin && (
            <div className="form-group">
              <label>Email Address</label>
              <input 
                type="email" 
                required 
                value={formData.email}
                onChange={(e) => setFormData({...formData, email: e.target.value})}
                placeholder="name@example.com"
              />
            </div>
          )}

          <div className="form-group">
            <label>Password</label>
            <input 
              type="password" 
              required 
              value={formData.password}
              onChange={(e) => setFormData({...formData, password: e.target.value})}
              placeholder="••••••••"
            />
          </div>

          <button type="submit" className="btn-primary auth-submit" disabled={loading}>
            {loading ? <span className="spinner"></span> : (isLogin ? 'Sign In' : 'Sign Up')}
          </button>
        </form>

        <div className="auth-footer">
          {isLogin ? "Don't have an account?" : "Already have an account?"}{' '}
          <button onClick={() => setIsLogin(!isLogin)} className="auth-toggle">
            {isLogin ? 'Create one now' : 'Log in here'}
          </button>
        </div>
      </div>

      <style>{`
        .auth-container {
          display: flex;
          align-items: center;
          justify-content: center;
          min-height: 80vh;
        }

        .auth-card {
          width: 100%;
          max-width: 420px;
          padding: 3rem 2.5rem;
          text-align: center;
        }

        .auth-header h2 {
          font-family: var(--f-display);
          font-size: 1.8rem;
          margin-bottom: 0.5rem;
          background: var(--grad-aurora);
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
        }

        .auth-header p {
          color: var(--text-3);
          font-size: 0.9rem;
          margin-bottom: 2rem;
        }

        .auth-form {
          text-align: left;
        }

        .form-group {
          margin-bottom: 1.25rem;
        }

        .form-group label {
          display: block;
          font-size: 0.8rem;
          font-weight: 600;
          color: var(--text-2);
          margin-bottom: 0.5rem;
          text-transform: uppercase;
          letter-spacing: 1px;
        }

        .form-group input {
          width: 100%;
          background: var(--bg-3);
          border: 1px solid var(--border-2);
          border-radius: var(--r-md);
          padding: 0.8rem 1rem;
          color: #fff;
          font-size: 0.95rem;
          transition: all 0.2s;
        }

        .form-group input:focus {
          outline: none;
          border-color: var(--accent-1);
          box-shadow: 0 0 0 4px rgba(124,58,237,0.1);
          background: var(--bg-4);
        }

        .auth-alert {
          background: rgba(239,68,68,0.1);
          border: 1px solid rgba(239,68,68,0.2);
          color: #fca5a5;
          padding: 0.8rem;
          border-radius: var(--r-md);
          font-size: 0.85rem;
          margin-bottom: 1.5rem;
        }

        .auth-alert.success {
          background: rgba(34,197,94,0.1);
          border: 1px solid rgba(34,197,94,0.2);
          color: #a3e7be;
        }

        .auth-submit {
          margin-top: 1rem;
          height: 50px;
        }

        .auth-footer {
          margin-top: 1.5rem;
          font-size: 0.88rem;
          color: var(--text-3);
        }

        .auth-toggle {
          background: none;
          border: none;
          color: var(--accent-3);
          font-weight: 600;
          cursor: pointer;
          padding: 0;
          margin-left: 5px;
        }

        .auth-toggle:hover {
          text-decoration: underline;
        }
      `}</style>
    </div>
  );
}
