import React, { createContext, useState, useEffect, useContext } from 'react';
import { login as loginService, logout as logoutService, getProfile as getProfileService, register as registerService, changePassword as changePasswordService } from './authService';
import { toast } from 'react-toastify';
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
        if (data) {
          console.log("Registration successful", data); 
          alert('Login successful!'); 
        }
        let userProfile;
        try {
            userProfile = await getProfileService();
            setUser(userProfile.data);
        } catch (profileError) {
            console.error("Profile fetch error:", profileError);  
        }
        setTimeout(() => {
            window.location.href = '/'; // Delay redirect to allow state update
        }, 200);
    } catch (error) {
        console.error("Login error:", error);
        alert("Invalid credentials");
    }
};

const register = async (userInfo) => {
  try {
    // Call the register service to make the API request
    const data = await registerService(userInfo); 

    if (data) {
      console.log("Registration successful", data); 
      alert('Registration successful!'); 
      toast.success('Registration successful!');
      window.location.href = '/login'; // Redirect to login page after successful registration 
    }
  } catch (error) {    
    console.error("Registration failed", error.message); 
    alert(`Registration failed: ${error.message}`);
  }
};

const logout = () => {
    logoutService();
    setUser(null);
    window.location.href= '/login'; // Redirect to login page after logout
};

// Change Password function
const changePassword = async (username, oldPassword, newPassword) => {
    try {
        const token = localStorage.getItem('access_token');
        if (!token) {
            alert("You must be logged in to change your password.");
            return;
        }

        await changePasswordService(username, oldPassword, newPassword); // Call your service to change the password
        alert('Password changed successfully!');
        logout(); // Redirect after password change
    } catch (error) {
        console.error('Error changing password:', error);
        alert('Error changing password. Please try again.');
    }
};


  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout, changePassword }}>
      {children}
    </AuthContext.Provider>
  );
};