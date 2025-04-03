import React, { createContext, useState, useEffect, useContext } from 'react';
import { login as loginService, logout as logoutService, getProfile as getProfileService, register as registerService, changePassword as changePasswordService } from './authService';
import { toast } from 'react-toastify';
import { useNavigate } from 'react-router-dom';
/*
 Author: Michael Tamatey/Navjot Kaur/Shohbit
 Date: 20250222
 Description: AUTHENTICATION CLASS
*/

const AuthContext = createContext();

export const useAuth = () => useContext(AuthContext);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

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
        .finally(() => setLoading(false));
    } else {
      setLoading(false); 
    }
  }, []);

  const login = async (credentials) => {
    try {
        const data = await loginService(credentials);
        if (data && data.access) {
          console.log("Registration successful", data);
          toast.success('Login successful!');

          localStorage.setItem('access_token', data.access);
          localStorage.setItem('refresh_token', data.refresh);

          try {
            const userProfile = await getProfileService(); 
            console.log("User profile fetched successfully", userProfile.data);
            setUser(userProfile.data);
            navigate('/');
        } catch (profileError) {
            console.error('Failed to fetch profile:', profileError);
            toast.error('Failed to fetch profile.');
        }
      } else {
          toast.error('Invalid login credentials');
      }
  } catch (error) {
      console.error('Login error:', error);
      toast.error(error.message || 'Login failed');
  }
};

const register = async (userInfo) => {
  try {
    // Call the register service to make the API request
    const data = await registerService(userInfo); 

    if (data) {
      console.log("Registration successful", data);       
      toast.success('Registration successful!');
      setTimeout(() => {
        navigate('/login');
      }, 2000); 
    }
  } catch (error) {    
    console.error("Registration failed", error.message); 
    toast.error(`Registration failed: ${error.message}`);
  }
};

const logout = () => {
    logoutService();
    setUser(null);
    toast.success('Logged out successfully');
    navigate('/login');
  };

// Change Password function
const changePassword = async (username, oldPassword, newPassword) => {
    try {
        const token = localStorage.getItem('access_token');
        if (!token) {
          toast.error("You must be logged in to change your password.");
            return;
        }

        await changePasswordService(username, oldPassword, newPassword);
        toast.success('Password changed successfully!');
        navigate('/login');
    } catch (error) {
        console.error('Error changing password:', error);
        toast.error('Error changing password. Please try again.');
    }
};


  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout, changePassword }}>
      {children}
    </AuthContext.Provider>
  );
};