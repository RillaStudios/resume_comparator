import axios from 'axios';
import { navigate } from 'react-router-dom';


/*
 Author: Michael Tamatey
 Date: 20250320
 Description: This function sets up Axios interceptors to handle authentication and error handling
*/

const setupAxiosInterceptors = () => {
  axios.interceptors.request.use(
    (config) => {
      const user = JSON.parse(localStorage.getItem('user'));
      if (user && user.accessToken) {
        config.headers.Authorization = `Bearer ${user.accessToken}`;
      }
      return config;
    },
    (error) => Promise.reject(error)
  );

  axios.interceptors.response.use(
    (response) => response,
    (error) => {
      if (error.response && error.response.status === 401) {
        localStorage.removeItem('user');
        navigate('/login'); // Redirect using React Router
      }
      return Promise.reject(error);
    }
  );
};

export default setupAxiosInterceptors;