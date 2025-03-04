import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import "./App.css";
import Layout from "./components/navbar/Layout";
import  MainPage  from "./components/mainPage/MainPage"; 
import Reports from "./components/pages/reports/Reports";
import Account from "./components/auth/Account";
import Summary from "./components/pages/summary/Summary";

/*
 Author: Michael Tamatey
 Date: 20250304
 Description: This class controls routes
*/

function App() {
  return (
    <Router>
      <Routes>
        {/* Wrap all routes inside Layout */}
        <Route path="/" element={<Layout />}>
          {/* Default Route */}
          <Route index element={<MainPage />} />
          <Route path="reports" element={<Reports />} />
          <Route path="account" element={<Account />} />
          <Route path="summary" element={<Summary />} />
        </Route>
      </Routes>
    </Router>
  );
}

export default App;
