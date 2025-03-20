import { useState, useCallback } from "react";
import axios from "axios";


/*
 Author: Michael Tamatey/ Navjot Kaur
 Date: 20250320
 Description: This class Configure the axios instance with the base URL and headers
*/


const apiClient = axios.create({
  baseURL: "http://localhost:8085/api", 
  headers: {
    "Content-Type": "application/json",
  },
});



export function useApi() {
  const [state, setState] = useState({
    data: undefined,
    loading: false,
    error: undefined,
  });


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


export function useApiWithJWT(jwtToken) {
  const [state, setState] = useState({
    data: undefined,
    loading: false,
    error: undefined,
  });

  const request = useCallback(async (config) => {
    if (!jwtToken) {
      setState({
        error: "No JWT Token available",
        loading: false,
      });
      return;
    }

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