import { useState } from 'react';
import axios from 'axios';
import './EnterEmail.css';

const EnterEmail = () => {
  const [email, setEmail] = useState('');
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://localhost:8000/api/verify_email/', { email });
      setMessage(response.data.message);
      setError('');
    } catch (error) {
      setError('There was an error sending the reset link.');
      setMessage('');
    }
  };

  return (
    <div className="email-reset-container">
      <h2 className="email-reset-header">Forgot Password - Resume Comparator</h2>
      <p className="email-reset-description">Please enter your email address to receive a password reset link soon.</p>
      <form onSubmit={handleSubmit}>
        <div className="email-reset-form-group">
          <input
            className="email-reset-input"
            type="email"
            id="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>
        <button className="email-reset-submit-btn" type="submit">Send Reset Link</button>
      </form>
      {message && <p className="email-reset-message email-reset-message-success">{message}</p>}
      {error && <p className="email-reset-message email-reset-message-error">{error}</p>}
    </div>
  );
};

export default EnterEmail;