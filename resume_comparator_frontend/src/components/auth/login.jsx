// src/pages/Login.jsx
import React, { useState } from 'react';
import { useAuth } from '../service/authContext';
import './auth.css';
import { toast } from "react-toastify";


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
      toast.success("Logged in successfully");
    } catch (err) {
      setError('Invalid credentials');
      toast.error("failed to login");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-page-container">
      <div className="login-page-left-section">
          <img
            src="src/assets/image/logo.png" 
            alt="Logo"
            className="login-page-branding-logo"
          />
      </div>
  
      <div className="login-page-right-section">
        <div >
          <h2>Welcome Back</h2>
          <form onSubmit={handleSubmit}>
          <input
            type="text"
            name="username"
            placeholder="Username"
            value={formData.username}
            onChange={handleChange}
            required
            className="input-field"
          />
        <input
            type="password"
            name="password"
           placeholder="Password"
           value={formData.password}
           onChange={handleChange}
           required
           className="input-field"
        />
        <div className="remember-me-container">
            <input type="checkbox" id="rememberMe" name="rememberMe" />
            <label htmlFor="rememberMe">Remember Me</label>
          </div>

          <a href="/register" className="change-password" >Don't have an account? Register here</a>
            {error && <p className="login-page-error-text">{error}</p>}
            <button
              type="submit"
              disabled={loading}
              className={`login-page-button ${loading ? 'processing' : ''}`}
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
