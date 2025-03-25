import React, { useState } from "react";
import "./reports.modules.css";

/*
 Author: Michael Tamatey/ Navjot Kaur
 Date: 20250222
 Description: This class allows users to view comparison results
*/

const Reports = () => {
  
  const [selectAll, setSelectAll] = useState(false);
  const [filter, setFilter] = useState("all")
  const [allReports, setAllReports] = useState([
  { date: "2025-03-01", name: "John Doe", score: 75, selected: false },
  { date: "2025-03-02", name: "Jane Smith", score: 55, selected: false },
  { date: "2025-03-03", name: "Bob Johnson", score: 65, selected: false },
  { date: "2025-03-04", name: "Alice Brown", score: 90, selected: false },
  { date: "2025-03-05", name: "Charlie Green", score: 50, selected: false },
  { date: "2025-03-06", name: "Daniel White", score: 72, selected: false },
  { date: "2025-03-07", name: "Emma Wilson", score: 95, selected: false },
  { date: "2025-03-08", name: "George Hall", score: 40, selected: false },
  ]);

  // Handle select all functionality
  const handleSelectAll = () => {
    setSelectAll(!selectAll);
    setAllReports((prevReports) =>
      prevReports.map((report) => ({
        ...report,
        selected: !selectAll,
      }))
    );
  };

  // Handle select one functionality
  const handleSelectOne = (index) => {
    const updatedReports = [...allReports];
    updatedReports[index].selected = !updatedReports[index].selected;
    setAllReports(updatedReports);
  };

  // Handle filter functionality
  const filteredReports = allReports.filter((report) => {
    if (filter === "passed") return report.score >= 70;
    if (filter === "failed") return report.score < 70;
    return true;
  });


  // Handle report item click
  const handleReportClick = (reportId) => {
    navigate(`/report-details/${reportId}`);  
  };

  return (
    <div className="reports-container">
      <h2>All Reports</h2>

  {/* Filter Dropdown */}
  <div className="filter-container">
        <label>Filter by Result: </label>
        <select value={filter} onChange={(e) => setFilter(e.target.value)}>
          <option value="all">All</option>
          <option value="passed">Passed</option>
          <option value="failed">Failed</option>
        </select>
      </div>

      {/* Select All Checkbox */}
      <div className="select-all">
        <label>
          <input
            type="checkbox"
            checked={selectAll}
            onChange={handleSelectAll}
          />
          Select All
        </label>
      </div>

      <div className="reports-list">
        {filteredReports.map((report, index) => (
          <div key={index} className="report-item">
          
            <div className="select-column">
              <input
                type="checkbox"
                checked={report.selected}
                onChange={() => handleSelectOne(index)}
              />
            </div>

            <div className="name-date-column">
              <div><strong>Name:</strong> {report.name}</div>
              <div><strong>Date:</strong> {report.date}</div>
            </div>

            <div className="score-column">
              <div><strong>Score:</strong> {report.score}%</div>
            </div>

            <div className="pass-fail-column">
              <strong>
                {report.score >= 70 ? "✅ Passed" : "❌ Failed"}
              </strong>
            </div>

            <div className="view-column">
              <button onClick={(e) => {
                e.stopPropagation(); 
                alert("View report");
              }}>📝</button>
            </div>
          </div>
        ))}
      </div>
    
     {/* Action Buttons */}
     
     <div className="action-buttons">
     <button onClick={() => alert("Emailing reports...")}>📧 Email</button>
     <button onClick={() => alert("Downloading reports...")}>📥 Download</button>
     <button onClick={() => alert("Deleting reports...")}>🗑️ Delete</button>
     <button onClick={() => alert("Printing reports...")}>🖨️ Print</button>
   </div>
   </div>
  );
};

export default Reports;

