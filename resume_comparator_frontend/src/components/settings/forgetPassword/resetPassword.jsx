import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';

const ResetPassword = () => {
  const { uidb64, token } = useParams();
  const [password, setPassword] = useState('');
  const [status, setStatus] = useState('');
  const [isValidLink, setIsValidLink] = useState(false);

  useEffect(() => {
    // Verify the reset link
    fetch(`http://localhost:8000/api/reset/${uidb64}/${token}/`)
      .then(res => res.json())
      .then(data => {
        if (data.error) {
          setStatus(data.error);
          setIsValidLink(false);
        } else {
          setStatus(data.message);
          setIsValidLink(true);
        }
      })
      .catch(err => {
        setStatus('Something went wrong while verifying the link.');
        setIsValidLink(false);
      });
  }, [uidb64, token]);

  const handleSubmit = async (e) => {
    e.preventDefault();

    const response = await fetch(`http://localhost:8000/api/reset/${uidb64}/${token}/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        new_password1: password,
        new_password2: password,
      }),
    });

    const data = await response.json();
    if (data.message) {
      setStatus(data.message);
      setIsValidLink(false); // disable form after success
    } else {
      setStatus(data.error || 'Error resetting password');
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100 px-4">
      <div className="w-full max-w-md bg-white shadow-md rounded-lg p-6">
        <h2 className="text-2xl font-semibold mb-4 text-center">Reset Your Password</h2>
        <p className="text-sm text-gray-600 mb-4 text-center">{status}</p>

        {isValidLink && (
          <form onSubmit={handleSubmit} className="space-y-4">
            <input
              type="password"
              placeholder="Enter new password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className="w-full px-4 py-2 border rounded-md"
            />
            <input
              type="password"
              placeholder="Confirm new password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className="w-full px-4 py-2 border rounded-md"
            />
            <button
              type="submit"
              className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 transition"
            >
              Reset Password
            </button>
          </form>
        )}
      </div>
    </div>
  );
};

export default ResetPassword;
