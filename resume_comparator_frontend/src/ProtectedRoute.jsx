import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import { useAuth } from './components/service/useAuth'; // Make sure this path is correct


/*
 Author: Michael Tamatey
 Date: 20250320
 Description: This component is used to protect routes that require authentication.
*/

const ProtectedRoute = () => {
  const { isAuthenticated } = useAuth();

  if (isAuthenticated === undefined) return <div>Loading...</div>; // Wait for authentication status

  return isAuthenticated ? <Outlet /> : <Navigate to="/login" replace />;
};

export default ProtectedRoute;