// src/pages/Login.jsx
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
  <div className="left-section">
  <div className="branding">
    <img
      src="src/assets/image/logo.png"  // <-- Change to your actual logo path (public folder)
      alt="Logo"
      className="branding-logo"
    />
    <h1 className="branding-title">Resume Comparator</h1>
  </div>
</div>

    <div className="upload-container">
      <form onSubmit={handleSubmit}>
        <h2>Login</h2>
        <input
          type="text"
          name="username"
          placeholder="Username"
          value={formData.username}
          onChange={handleChange}
          required
        />
        <input
          type="password"
          name="password"
          placeholder="Password"
          value={formData.password}
          onChange={handleChange}
          required
        />
        {error && <p className="error-text">{error}</p>}
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
