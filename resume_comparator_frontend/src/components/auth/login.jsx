// src/pages/LoginPage.jsx
import React, { useState } from 'react';
import { useAuth } from '../service/authContext';
import './auth.css'; // Reuse shared layout CSS
import { login } from '../service/authService'; // Use the provided API service

const LoginPage = () => {
  const [formData, setFormData] = useState({ username: '', password: '' });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const {login} = useAuth();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      await login(formData); // Calls the abstracted login from your authService
      window.location.href= '/';
    } catch (err) {
      setError('Invalid credentials');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="main-container">
      <div className="container-body">
        {/* Branding Section */}
        <div className="left-section">
          <h1 className="user-d">Resume Comparator</h1>
        </div>

        {/* Login Form Section */}
        <div className="upload-container">
          <form onSubmit={handleSubmit} style={{ width: '100%' }}>
            <h2 style={{ marginBottom: '10px' }}>Login</h2>
            <input
              type="text"
              name="username"
              placeholder="Username"
              value={formData.username}
              onChange={handleChange}
              required
              style={{ width: '100%', padding: 10, marginBottom: 10 }}
            />
            <input
              type="password"
              name="password"
              placeholder="Password"
              value={formData.password}
              onChange={handleChange}
              required
              style={{ width: '100%', padding: 10, marginBottom: 10 }}
            />
            {error && <p style={{ color: 'red' }}>{error}</p>}
            <button
              type="submit"
              disabled={loading}
              className={`convert-button ${loading ? 'processing' : ''}`}
            >
              {loading ? 'Logging in...' : 'Login'}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;
