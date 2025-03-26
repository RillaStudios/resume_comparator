import React, { useState } from 'react';
import { useAuth } from '../service/authContext';

const Login = () => {
  const [username, setUserName] = useState('');
  const [password, setPassword] = useState('');
  const { login } = useAuth();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await login({ username, password });
      window.location.href = '/';
    } catch (error) {
      console.error('Login failed', error);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input 
        type="username" 
        placeholder="username" 
        value={username} 
        onChange={(e) => setUserName(e.target.value)} 
        required 
      />
      <input 
        type="password" 
        placeholder="Password" 
        value={password} 
        onChange={(e) => setPassword(e.target.value)} 
        required 
      />
      <button type="submit">Login</button>
    </form>
  );
};

export default Login;
