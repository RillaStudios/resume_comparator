import React, { useState, useEffect } from "react";
import "./reports.modules.css";
import { toast } from "react-toastify";
import { useLocation, useNavigate } from "react-router-dom";

/*
 Author: Michael Tamatey / Navjot Kaur
 Date: 20250222
 Description: This class allows users to view comparison results
*/

const Reports = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { jobTitle, score, created_at } = location.state || {}; // Retrieve job title & score

  const [selectAll, setSelectAll] = useState(false);
  const [filter, setFilter] = useState("all");
  const [allReports, setAllReports] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Fetch reports from database
  useEffect(() => {
    const fetchReports = async () => {
      try {
        const response = await fetch("http://127.0.0.1:8000/api/reports/");
        if (!response.ok) throw new Error("Failed to fetch reports");
        const data = await response.json();
        setAllReports(data.map(report => ({ ...report, selected: false }))); // Ensure selected is false initially
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchReports();
  }, []);

  // Handle Select All functionality
  const handleSelectAll = () => {
    setAllReports(prevReports =>
      prevReports.map(report => ({ ...report, selected: !selectAll }))
    );
    setSelectAll(!selectAll);
  };

  // Handle individual report selection
  const handleSelectOne = id => {
    setAllReports(prevReports =>
      prevReports.map(report =>
        report.id === id ? { ...report, selected: !report.selected } : report
      )
    );
  };

  // Filter reports based on user selection
  const filteredReports = allReports.filter(report => {
    if (filter === "passed") return report.score >= 7;
    if (filter === "failed") return report.score < 7;
    return true;
  });

  // Handle Delete Reports functionality
  const handleDeleteReports = async () => {
    const selectedReports = filteredReports.filter((report) => report.selected);
    if (selectedReports.length === 0) {
      toast.error("No reports selected! Please select at least one.");
      return;
    }
  
    try {
      await Promise.all(
        selectedReports.map((report) =>
          fetch(`http://127.0.0.1:8000/api/reports/${report.id}/`, {
            method: "DELETE",
          })
        )
      );
  
      toast.success("Reports deleted successfully!");
      setAllReports((prevReports) => prevReports.filter((report) => !report.selected));
    } catch (error) {
      toast.error("Failed to delete reports.");
      console.error("Delete error:", error);
    }
  };

  // Fix: Ensure handleReportClick accepts an ID
  const handleReportClick = id => {
    navigate(`/summary/${id}`); // Navigate to summary page with report ID
  };

  return (
    <div className="reports-container">
      <h2>All Reports</h2>

      {/* Show Loading/Error */}
      {loading && <p>Loading reports...</p>}
      {error && <p className="error">{error}</p>}

      {!loading && !error && (
        <>
          {/* Filter Dropdown */}
          <div className="filter-container">
            <label>Filter by Result: </label>
            <select value={filter} onChange={e => setFilter(e.target.value)}>
              <option value="all">All</option>
              <option value="passed">Passed</option>
              <option value="failed">Failed</option>
            </select>
          </div>

          {/* Select All Checkbox */}
          <div className="select-all">
            <label>
              <input type="checkbox" checked={selectAll} onChange={handleSelectAll} />
              Select All
            </label>
          </div>

          {/* No Data Message */}
          {filteredReports.length === 0 ? (
            <p className="no-data">No information to display</p>
          ) : (
            <>
              {/* Reports List */}
              <div className="reports-list">
                {filteredReports.map(report => (
                  <div key={report.id} className="report-item">
                    <div className="select-column">
                      <input
                        type="checkbox"
                        checked={report.selected || false} // Ensure it starts as controlled
                        onChange={e => {
                          e.stopPropagation();
                          handleSelectOne(report.id);
                        }}
                      />
                    </div>

                    <div className="name-date-column">
                      <div>
                      <div><strong>Job:</strong> {jobTitle ? jobTitle : report.jobTitle}</div>
                      </div>

                      <strong>Date:</strong>{" "}
                      {created_at || report.created_at
                        ? new Date(report.created_at).toLocaleDateString()
                        : "N/A"}
                    </div>

                    <div className="score-column">
                      <strong>Score:</strong>{" "}
                      {Math.min(10, ((score || report.score) / 10).toFixed(1))} / 10
                    </div>

                    <div className="pass-fail-column">
                      <strong>{report.score >= 7 ? "✅ Passed" : "❌ Failed"}</strong>
                    </div>

                    <div className="view-column">
                      <button onClick={() => handleReportClick(report.id)}>📝</button>
                    </div>
                  </div>
                ))}
              </div>

              {/* Action Buttons */}
              <div className="action-buttons">
                <button onClick={() => handleEmailReports("Emailing")}>📧 Email</button>
                <button onClick={() => handleDownloadReports("Downloading")}>📥 Download</button>
                <button onClick={handleDeleteReports}>🗑️ Delete</button>
                <button onClick={() => handlePrintingReports("Printing")}>🖨️ Print</button>
              </div>
            </>
          )}
        </>
      )}
    </div>
  );
};

export default Reports;