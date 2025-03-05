import React from "react";
import { useLocation } from "react-router-dom";
 import "./Reports.modules.css";


/*
 Author: Michael Tamatey/ Navjot Kaur
 Date: 20250222
 Description: This class allows users to view comparison results
*/

const Reports = () => {
  const location = useLocation();
  const { jobTitle, score } = location.state || {}; // Retrieve data

  // Determine pass/fail
  const status = score >= 80 ? "✅ Passed" : "❌ Failed";

  return (
    <div className="reports-container">
      <h2>Comparison Results</h2>
      <p><strong>Job Title:</strong> {jobTitle}</p>
      <p><strong>Score:</strong> {score}%</p>
      <p><strong>Result:</strong> {status}</p>
    </div>
  );
};

export default Reports;
