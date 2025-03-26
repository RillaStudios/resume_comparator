import React, { createContext, useState, useEffect, useContext } from 'react';
import { login as loginService, logout as logoutService, getProfile as getProfileService } from './authService';

const AuthContext = createContext();

export const useAuth = () => useContext(AuthContext);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (token) {
      getProfileService().then(response => {
        setUser(response.data);
      }).catch(() => {
        logout();
      });
    }
  }, []);

  const login = async (credentials) => {
    try {
      const data = await loginService(credentials);
      const userProfile = await getProfileService();
      setUser(userProfile.data);
      window.location.href = '/';
    } catch (error) {
      console.error("Login failed", error);
    }
  };

  const logout = () => {
    logoutService();
    setUser(null);
    navigate('/login'); // Redirect to login page after logout
  };

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

