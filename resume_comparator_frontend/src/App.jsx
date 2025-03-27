import React from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import "./App.css";
import MainPage from "./components/mainPage/mainPage";
import Reports from "./components/pages/reports/Reports";
import Summary from "./components/pages/summary/summary";
import Account from "./components/settings/account/account";
import DashboardLayout from "./DashboardLayout";
import NotFound from "./components/auth/notFound";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import { AuthProvider, useAuth } from "./components/service/authContext"; // Make sure to import useAuth
import Login from "./components/auth/login";

/*
 Author: Michael Tamatey/ Navjot Kaur
 Date: 20250222
 Description: This class controls routes
*/

// 🔐 Protected Route Component
const ProtectedRoute = ({ element }) => {
  const { user, loading } = useAuth();

  if (loading) return <div>Loading...</div>; // Show loading while fetching profile

  return user ? element : <Navigate to="/login" replace />;
};

function App() {
  return (
    <AuthProvider>
      {/* Toast Notifications */}
      <ToastContainer
        position="top-center"
        autoClose={3000}
        hideProgressBar={false}
        newestOnTop={true}
        closeOnClick
        rtl={false}
        pauseOnFocusLoss
        draggable
        pauseOnHover
        theme="colored"
      />

      <Router>
        <Routes>
          {/* Public Route: Login */}
          <Route path="/login" element={<Login />} />

          {/* Private Routes */}
          <Route path="/" element={<ProtectedRoute element={<DashboardLayout />} />}>
            <Route index element={<MainPage />} />
            <Route path="reports" element={<Reports />} />
            <Route path="summary" element={<Summary />} />
            <Route path="account" element={<Account />} />
          </Route>

          {/* 404 Page */}
          <Route path="*" element={<NotFound />} />
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;