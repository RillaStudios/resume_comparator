import axios from 'axios';
/*
 Author: Michael Tamatey
 Date: 20250320
 Description: This class Configure the axios instance with the base URL and headers
*/


// Base API URL
const API_URL = 'http://localhost:8000/api'; 

// Register User
export const register = async (userData) => {
    return await axios.post(`${API_URL}/register/`, userData);
};

// Login User
export const login = async (credentials) => {
    const response = await axios.post(`${API_URL}/login/`, credentials);
    if (response.data.access) {
        localStorage.setItem('access_token', response.data.access);
        localStorage.setItem('refresh_token', response.data.refresh);
    }
    return response.data;
};

// Logout User
export const logout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
};

// Get User Profile
export const getProfile = async () => {
    const token = localStorage.getItem('access_token');
    return await axios.get(`${API_URL}/profile/`, {
        headers: { Authorization: `Bearer ${token}` }
    });
};

// Change Password
export const changePassword = async (newPassword) => {
    const token = localStorage.getItem('access_token');
    return await axios.post(`${API_URL}/profile/changepass/`, { new_password: newPassword }, {
        headers: { Authorization: `Bearer ${token}` }
    });
};

// Delete Account
export const deleteAccount = async (password) => {
    const token = localStorage.getItem('access_token');
    return await axios.post(`${API_URL}/profile/delete/`, { password }, {
        method: 'DELETE',
        headers: { Authorization: `Bearer ${token}` }
    });
};