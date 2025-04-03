import React, { createContext, useState, useEffect, useContext } from 'react';
import { login as loginService, logout as logoutService, getProfile as getProfileService, register as registerService, changePassword as changePasswordService } from './authService';
import { toast } from 'react-toastify';
import { useNavigate } from 'react-router-dom';
/*
 Author: Michael Tamatey/ Navjot Kaur
 Date: 20250222
 Description: AUTHENTICATION CLASS
*/

const AuthContext = createContext();

export const useAuth = () => useContext(AuthContext);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true); // Track loading state
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
        .finally(() => setLoading(false)); // Set loading to false
    } else {
      setLoading(false); // No token, stop loading
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
            const userProfile = await getProfileService();  //  Ensure this is called only when login is successful
            console.log("User profile fetched successfully", userProfile.data);
            setUser(userProfile.data);  //  Save user profile in context
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
      // alert('Registration successful!'); 
      toast.success('Registration successful!');
      // window.location.href = '/login'; // Redirect to login page after successful registration 
      setTimeout(() => {
        navigate('/login'); // Navigate only after toast is shown
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
    // window.location.href= '/login'; // Redirect to login page after logout
    toast.success('Logged out successfully'); //  Toast notification for logout
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

        await changePasswordService(username, oldPassword, newPassword); // Call your service to change the password
        toast.success('Password changed successfully!');
        logout(); // Redirect after password change
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