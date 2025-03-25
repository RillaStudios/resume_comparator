import axios from 'axios';


/*
 Author: Michael Tamatey/ Navjot Kaur
 Date: 20250320
 Description: This class Configure the axios instance with the base URL and headers
*/


const API_URL = 'http://localhost:8085/api/auth/';

const register = (firstName, lastName, email, password, address) => {
  return axios.post(API_URL + 'signup', {
    firstName,
    lastName,
    email,
    password,
    address,
    role: 'DIRECTOR', // Default role to 'DIRECTOR'
  });
};

const login = async (username, password) => {
  try {
    const response = await axios.post(API_URL + 'signin', {
      username,
      password,
    });

    if (response.data.accessToken) {
      localStorage.setItem('user', JSON.stringify(response.data));
    }

    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.message || "Login failed");
  }
};

const logout = () => {
  localStorage.removeItem('user');
};

const getCurrentUser = () => {
  return JSON.parse(localStorage.getItem('user'));
};

const authService = {
  register,
  login,
  logout,
  getCurrentUser,
};

export default authService;