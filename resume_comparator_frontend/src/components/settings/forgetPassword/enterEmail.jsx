import { useState } from 'react';
import axios from 'axios';
import './EnterEmail.css';
import spinner from "../../../assets/image/loadingSpinner.gif";



const EnterEmail = () => {
  const [email, setEmail] = useState('');
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [emailSent, setEmailSent] = useState(false); 
  

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setEmailSent(false);
    
    try {
      const response = await axios.post('http://localhost:8000/api/verify_email/', { email });
      setMessage('Reset link sent! Please check your email.');
      setEmailSent(true);
      setEmail(''); 
      setError('');
    } catch (error) {
      setError('There was an error sending the reset link.');
      setMessage('');
      setEmailSent(false);
    }setTimeout(() => {
      setLoading(false);
    }, 1000);
  };

  return (
    <div className="email-reset-container">
      <h2 className="email-reset-header">Forgot Password - Resume Comparator</h2>
      <p className="email-reset-description">Please enter your email address to receive a password reset link.</p>
      <form onSubmit={handleSubmit}>
        <div className="email-reset-form-group">
          <input
            className="email-reset-input"
            type="email"
            id="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            placeholder='Enter your email'
          />
        </div>
      <button
          type="submit"
          disabled={loading}
          className={`email-reset-submit-btn 
              ${loading ? 'processing' : ''} 
              ${emailSent ? 'sent' : ''}`}
>
  {loading ? 'Processing...' : emailSent ? 'Sent' : 'Send Reset Link'}
</button>
        {loading && (
                  <div className="loading-spin">
                    <div className="loading-spinner">
                      <img src={spinner} alt="Loading..." />
                    </div>
                  </div>
                   )}
      </form>
      {message && <p className="email-reset-message email-reset-message-success">{message}</p>}
      {error && <p className="email-reset-message email-reset-message-error">{error}</p>}
    
    </div>
  );
};

export default EnterEmail;