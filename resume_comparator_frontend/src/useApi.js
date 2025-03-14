import { useState, useCallback } from "react";
import apiClient from "./components/service/api"; // Ensure you have an Axios instance configured


// Custom hook to handle API requests
// This hook is used to make API requests and manage the state of the request (loading, data, error)
export function useApi() {
  const [state, setState] = useState({
    data: undefined,
    loading: false,
    error: undefined,
  });


    // Function to make an API request
  const request = useCallback(async (config) => {
    setState({ loading: true, error: undefined });

    try {
      const response = await apiClient(config);
      setState({ data: response.data, loading: false });
      return response.data;
    } catch (err) {
      setState({
        error: err.response?.data?.message || "Something went wrong",
        loading: false,
      });
      throw err;
    }
  }, []);

  return { ...state, request };
}

// Custom hook to handle API requests with JWT token
export function useApiWithJWT(jwtToken) {
  const [state, setState] = useState({
    data: undefined,
    loading: false,
    error: undefined,
  });

  const request = useCallback(async (config) => {
    setState({ loading: true, error: undefined });

    try {
      const headers = {
        Authorization: `Bearer ${jwtToken}`,
        ...config.headers,
      };

      const response = await apiClient({ ...config, headers });
      setState({ data: response.data, loading: false });
      return response.data;
    } catch (err) {
      setState({
        error: err.response?.data?.message || "Something went wrong",
        loading: false,
      });
      throw err;
    }
  }, [jwtToken]);

  return { ...state, request };
}
