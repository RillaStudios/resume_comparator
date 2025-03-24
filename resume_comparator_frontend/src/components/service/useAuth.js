import { useState, useEffect } from 'react';


/*
 Author: Michael Tamatey/ Navjot Kaur
 Date: 20250320
 Description: This function sets up the authentication hook
*/
export const useAuth = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(undefined);

  useEffect(() => {
    const token = localStorage.getItem("token");
    setIsAuthenticated(!!token);
  }, []);

  return { isAuthenticated };
};