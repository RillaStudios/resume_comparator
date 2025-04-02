// src/pages/Login.jsx
import React, { useEffect, useState } from 'react';
import { useAuth } from '../service/authContext';
import { Eye, EyeOff } from "lucide-react"; // Import eye icons
import './auth.css';
import { toast } from "react-toastify";
import spinner from "../../assets/image/loadingSpinner.gif";
import { useNavigate } from 'react-router-dom'; 

const LoginPage = () => {
  const [formData, setFormData] = useState({ username: '', password: '' });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();
  const [rememberMe, setRememberMe] = useState(false);
  const [showPassword, setShowPassword] = useState(false); // State for password visibility

  // Load the saved state from localStorage when the component mounts
  useEffect(() => {
    const savedRememberMe = localStorage.getItem('rememberMe') === 'true';
    setRememberMe(savedRememberMe);
  }, []);

  // Handle checkbox change
  const handleRememberMeChange = (e) => {
    const isChecked = e.target.checked;
    setRememberMe(isChecked);
    localStorage.setItem('rememberMe', isChecked); // Save to localStorage
  };

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
  
    if (!formData.username || !formData.password) {
      setError('Login Failed');
      toast.error("Login Failed");
      setLoading(false); // Stop loading if validation fails
      return;
    }
  
    try {
      await login({username: formData.username, password: formData.password}); // Ensure `login` throws an error if authentication fails
      // navigate('/');
      
    } catch (err) {
      console.error("Login Error:", err);
      setError('Invalid credentials');
      toast.error("Failed to login");
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
        <div>
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

            {/* Password Input with Visibility Toggle */}
            <div className="password-container1">
              <input
                type={showPassword ? "text" : "password"}
                name="password"
                placeholder="Password"
                value={formData.password}
                onChange={handleChange}
                required
                className="input-field"
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="toggle-password"
              >
                {showPassword ? <EyeOff size={20} /> : <Eye size={20} />}
              </button>
            </div>

            <div className="remember-me-container">
              <input
                type="checkbox"
                id="rememberMe"
                name="rememberMe"
                checked={rememberMe}
                onChange={handleRememberMeChange} // Update state on change
              />
              <label htmlFor="rememberMe">Remember Me</label>
            </div>
            
            {error && <p className="login-page-error-text">{error}</p>}
            
            <button
              type="submit"
              disabled={loading}
              className={`login-page-button ${loading ? 'processing' : ''}`}
            >
              {loading ? 'Logging in...' : 'Login'}
            </button>

            <a href="/register" className="change-password">Don't have an account? Register here</a>
            {loading && (
              <div className="loading-spin">
                <div className="loading-spinner">
                  <img src={spinner} alt="Loading..." />
                </div>
              </div>
            )}
          </form>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;