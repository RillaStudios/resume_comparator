import React, { createContext, useState, useEffect, useContext } from 'react';
import { login as loginService, logout as logoutService, getProfile as getProfileService, register as registerService } from './authService';


/*
 Author: Michael Tamatey
 Date: 20250222
 Description: AUTHENTICATION CLASS
*/

const AuthContext = createContext();

export const useAuth = () => useContext(AuthContext);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true); // Track loading state
  

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (token) {
      getProfileService()
        .then(response => {
          setUser(response.data);
        })
        .catch(() => {
          logout();
        })
        .finally(() => setLoading(false)); // Set loading to false
    } else {
      setLoading(false); // No token, stop loading
    }
  }, []);

  const login = async (credentials) => {
    try {
        const data = await loginService(credentials);
        const userProfile = await getProfileService();
        
        setUser(userProfile.data); // Update user state first

        setTimeout(() => {
            window.location.href = '/'; // Delay redirect to allow state to update
        }, 200); 
    } catch (error) {
        console.error("Login failed", error);
    }
};

const register = async (userInfo) => {
  try {
    const data = await registerService(userInfo); // Call the register service
    if (data) {
      window.location.href = '/login'; // Redirect to login page after successful registration
    }
  } catch (error) {
    console.error("Registration failed", error);
  }
};

  const logout = () => {
    logoutService();
    setUser(null);
    window.location.href= '/login'; // Redirect to login page after logout
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

