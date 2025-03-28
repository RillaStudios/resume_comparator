import React, { useState } from 'react';
import { useAuth } from '../service/authContext';
import './authRegister.css';
import { toast } from "react-toastify";
import spinner from "../../assets/image/loadingSpinner.gif";
import { Eye, EyeOff } from "lucide-react"; // Import icons for password visibility toggle

const RegisterPage = () => {
  const [formData, setFormData] = useState({
    username: '',
    first_name: '',
    last_name: '',
    email: '',
    address: '',
    role: 'RECRUITER', // Default role
    password: '',
    confirm_password: '',
  });
  
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { register } = useAuth(); // Call register from your auth context
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    
    // Check for password match
    if (formData.password !== formData.confirm_password) {
      setError('Passwords do not match');
      toast.error('Passwords do not match');
      return;
    }
  
    setLoading(true);
  
    try {
      // Call register function from authContext
      await register(formData);
    } catch (err) {
      // Handle errors by displaying specific error messages
      setError(err.message || 'Registration failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="register-page-container">
      <div className="register-page-left-section">
        <img
          src="src/assets/image/logo.png"
          alt="Logo"
          className="register-page-branding-logo"
        />
      </div>

      <div className="register-page-right-section">
        <div>
          <h2>Create an Account</h2>
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
              type="text"
              name="first_name"
              placeholder="First Name"
              value={formData.first_name}
              onChange={handleChange}
              required
              className="input-field"
            />
            <input
              type="text"
              name="last_name"
              placeholder="Last Name"
              value={formData.last_name}
              onChange={handleChange}
              required
              className="input-field"
            />
            <input
              type="email"
              name="email"
              placeholder="Email"
              value={formData.email}
              onChange={handleChange}
              required
              className="input-field"
            />
            <input
              type="text"
              name="address"
              placeholder="Address"
              value={formData.address}
              onChange={handleChange}
              required
              className="input-field"
            />
            
            {/* Role Dropdown */}
            <select
              name="role"
              value={formData.role}
              onChange={handleChange}
              className="input-field"
            >
              <option value="RECRUITER">RECRUITER</option>
              <option value="DIRECTOR">DIRECTOR</option>
            </select>

            {/* Password Field with Toggle */}
            <div className="password-container">
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

            {/* Confirm Password Field with Toggle */}
            <div className="password-container">
              <input
                type={showConfirmPassword ? "text" : "password"}
                name="confirm_password"
                placeholder="Confirm Password"
                value={formData.confirm_password}
                onChange={handleChange}
                required
                className="input-field"
              />
              <button
              type="button"
              onClick={() => setShowConfirmPassword(!showConfirmPassword)}
              className="toggle-password"
              >
                {showConfirmPassword? <EyeOff size={20} /> : <Eye size={20} />}
              </button>
              
            </div>

            <a href="/login" className="change-password">Already have an account? Login here</a>
            <br />

            {error && <p className="register-page-error-text">{error}</p>}
            <button
              type="submit"
              disabled={loading}
              className={`register-page-button ${loading ? 'processing' : ''}`}
            >
              {loading ? 'Registering...' : 'Register'}
            </button>
            
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

export default RegisterPage;
