import axios from 'axios';
/*
 Author: Michael Tamatey/Navjot Kaur/Shohbit
 Date: 20250320
 Description: This class Configure the axios instance with the base URL and headers
*/


// Base API URL
const API_URL = 'http://localhost:8000/api'; 

// Register User
export const register = async (userData) => {
    try {
      const response = await axios.post(`${API_URL}/register/`, userData);
      return response.data;  
    } catch (error) {
      if (error.response) {
        const errorMessage = error.response.data.message || error.response.data.error || 'Registration failed';
        throw new Error(errorMessage);
      } else if (error.request) {
        throw new Error('No response from server');
      } else {
        throw new Error(error.message || 'Something went wrong during registration');
      }
    }
  };
// Login User
export const login = async (credentials) => {
    try {
        const formData = new URLSearchParams();
        formData.append('username', credentials.username);
        formData.append('password', credentials.password);

        const response = await axios.post(
            `${API_URL}/login/`, 
            formData,
            {
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                }
            }
        );

        if (response.data.access) {
            return response.data;
        }

        throw new Error('Login failed. Tokens not received.');
    } catch (error) {
        console.error('Login failed', error.response?.data || error.message);
        throw new Error(error.response?.data?.error || 'Invalid credentials');
    }
};

// Logout User
export const logout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
};

// Get User Profile
export const getProfile = async () => {
    const token = localStorage.getItem('access_token');
    if (!token) {
        throw new Error('No access token found');
    }

    try {
        const response = await axios.get(`${API_URL}/profile/`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        return response;
    } catch (error) {
        console.error('Failed to fetch profile', error);
        throw error;
    }
};

// Change Password
export const changePassword = async (username, oldPassword, newPassword) => {
    const token = localStorage.getItem('access_token');
    
    if (!token) {
        throw new Error("Authentication token missing. Please log in again.");
    }

    try {
        const response = await axios.post(
            `${API_URL}/profile/changepass/`, 
            { 
                username: username,
                old_password: oldPassword, 
                new_password: newPassword 
            }, 
            { 
                headers: { Authorization: `Bearer ${token}` }
            }
        );
        
        return response.data;
    } catch (error) {
        console.error("Error changing password:", error.response?.data || error.message);
        throw new Error(error.response?.data?.error || "Error changing password. Please try again.");

    }
};

// Delete Account
export const deleteAccount = async (password) => {
    const token = localStorage.getItem('access_token');
    return await axios.post(`${API_URL}/profile/delete/`, { password }, {
        method: 'DELETE',
        headers: { Authorization: `Bearer ${token}` }
    });
};