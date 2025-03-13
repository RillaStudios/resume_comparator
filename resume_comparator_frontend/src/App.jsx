import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import "./App.css";
import  MainPage  from "./components/mainPage/mainPage"; 
import Reports from "./components/pages/reports/reports";
import Summary from "./components/pages/summary/summary";
import Account from "./components/settings/account/account";
import DashboardLayout from "./DashboardLayout";
import NotFound from "./components/auth/notFound";
import { ToastContainer} from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

/*
 Author: Michael Tamatey/ Navjot Kaur
 Date: 20250222
 Description: This class controls routes
*/

function App() {
  return (
    <> 
    {/* Toast Notifications */}
    <ToastContainer position="top-center" // Positions the popup in the center
        autoClose={3000} // Auto closes after 3 seconds
        hideProgressBar={false} // Show progress bar
        newestOnTop={true} // New toasts appear on top
        closeOnClick // Close on click
        rtl={false} // Left to right
        pauseOnFocusLoss // Pause when user switches tab
        draggable // Allow dragging
        pauseOnHover // Pause on hover
        theme="colored" // Use colored theme
         /> 

         {/* Routes */}
    <Router>
      <Routes>  
        <Route path="/" element={<DashboardLayout />}>
          <Route index element={<MainPage />} />
          <Route path="/reports" element={<Reports />} />
          <Route path="/summary" element={<Summary />} />
          <Route path="/account" element={<Account />} />
          

        </Route>

        {/* 404 Page - Must be the last route */}
        {<Route path="*" element={<NotFound />} />}
      </Routes>
    </Router>
    </>
  );
}

export default App;