import React, { createContext, useState, useEffect, useContext } from 'react';
import { login as loginService, logout as logoutService, getProfile as getProfileService, register as registerService, changePassword as changePasswordService } from './authService';
import { toast } from 'react-toastify';
/*
 Author: Michael Tamatey/Navjot Kaur/shobhit
 Date: 20250222
 Description: AUTHENTICATION CLASS
*/

const AuthContext = createContext();

export const useAuth = () => useContext(AuthContext);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

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
        if (data) {
          console.log("Login Successful", data); 
          toast.success('Login successful!'); 
        }
        let userProfile;
        try {
            userProfile = await getProfileService();
            setUser(userProfile.data);
        } catch (profileError) {
            console.error("Profile fetch error:", profileError);  
        }
        setTimeout(() => {
            window.location.href = '/';
        }, 350);
    } catch (error) {
        console.error("Login error:", error);
        toast.error("Invalid credentials"); 
    }
};

const register = async (userInfo) => {
  try {
    // Call the register service to make the API request
    const data = await registerService(userInfo); 

    if (data) {
      console.log("Registration successful", data); 
      toast.success('Registration successful!');
      window.location.href = '/login'; 
    }
  } catch (error) {    
    console.error("Registration failed", error.message); 
    toast.error(`Registration failed: ${error.message}`);
  }
};

const logout = () => {
    logoutService();
    setUser(null);
    window.location.href= '/login';
};

// Change Password function
const changePassword = async (username, oldPassword, newPassword) => {
    try {
        const token = localStorage.getItem('access_token');
        if (!token) {
            toast.error("You must be logged in to change your password.");
            return;
        }

        // Call your service to change the password
        await changePasswordService(username, oldPassword, newPassword); 
        toast.success('Password changed successfully!');
        logout();
    } catch (error) {
        console.error('Error changing password:', error);
        alert('Error changing password. Please try again.');
        toast.error('Error changing password. Please try again.');
    }
};


  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout, changePassword }}>
      {children}
    </AuthContext.Provider>
  );
};