import axios from "axios";

const API_BASE_URL = "http://localhost:8050/api";

// Create an Axios instance with default settings
export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Function to retrieve JWT token from local storage
const getAuthToken = () => localStorage.getItem("token");

// Attach JWT token to every request if available
apiClient.interceptors.request.use((config) => {
  const token = getAuthToken();
  if (token) {
    config.headers = {
      ...config.headers, // Preserve existing headers
      Authorization: `Bearer ${token}`,
    };
  }
  return config;
});

// Handle unauthorized responses (e.g., expired token)
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      console.error("Unauthorized! Redirecting to login...");
      localStorage.removeItem("token");
      window.location.href = "/login"; // Redirect to login page
    }
    return Promise.reject(error);
  }
);