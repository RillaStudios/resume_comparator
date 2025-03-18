import React, { useState, useEffect } from "react";
import { useLocation } from "react-router-dom";
import "./reports.modules.css";


/*
 Author: Michael Tamatey/ Navjot Kaur
 Date: 20250222
 Description: This class allows users to view comparison results
*/

const Reports = () => {
  const location = useLocation();
  const { jobTitle, score } = location.state || {}; // Retrieve data

  // Determine pass/fail
  const status = score >= 0.70 ? "✅ Passed" : "❌ Failed";

  const [allReports, setAllReports] = useState([]);

  useEffect(() => {
    // Fetch all reports when no specific report is selected
    if (!score && !jobTitle) {
      fetch('http://localhost:8000/api/reports')
        .then(response => response.json())
        .then(data => setAllReports(data))
        .catch(error => console.error('Error fetching reports:', error));
    }
  }, [score, jobTitle]);

  return (
    <div className="reports-container">
      {score && jobTitle ? (
        // Show single report
        <>
          <h2>Comparison Results</h2>
          <p><strong>Job Title:</strong> {jobTitle}</p>
          <p><strong>Score:</strong> {score}%</p>
          <p><strong>Result:</strong> {status}</p>
        </>
      ) : (
        // Show all reports
        <>
          <h2>All Reports</h2>
          <div className="reports-list">
            {allReports.map((report, index) => (
              <div key={index} className="report-item">
                <p><strong>Job Id:</strong> {report.job_id}</p>
                <p><strong>Score:</strong> {report.score}%</p>
                <p><strong>Result:</strong> {report.score >= 0.70 ? "✅ Passed" : "❌ Failed"}</p>
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  );
};

export default Reports;
