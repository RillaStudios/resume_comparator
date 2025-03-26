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
  const { jobTitle, score, created_at, job_id } = location.state || {}; // Retrieve job title & score

  const [selectAll, setSelectAll] = useState(false);
  const [filter, setFilter] = useState("all");
  const [allReports, setAllReports] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [dialogVisible, setDialogVisible] = useState(false);
  const [actionType, setActionType] = useState(""); 

  // Fetch reports from database
  useEffect(() => {
    const fetchReports = async () => {
      try {
        const response = await fetch("http://127.0.0.1:8000/api/reports/");
        if (!response.ok) throw new Error("Failed to fetch reports");
        const data = await response.json();
        setAllReports(data.map(report => ({ ...report, selected: false }))); 
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


  // Handle Download Report functionality
  const handleDownloadReports = async () => {
    const selectedReports = filteredReports.filter((report) => report.selected);
    if (selectedReports.length === 0) {
      toast.error("No reports selected! Please select at least one.");
      return;
    }
  
    try {
      const reportIds = selectedReports.map((report) => report.id).join(",");
  
      const response = await fetch(`http://127.0.0.1:8000/api/reports/download?report_ids=${reportIds}`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      });
  
      if (!response.ok) {
        throw new Error("Failed to download reports.");
      }
  
      // Check the content type of the response
      const contentType = response.headers.get("Content-Type");
  
      if (contentType && contentType.includes("application/zip")) {
        // If the response is a ZIP file
        const blob = await response.blob();
        const fileUrl = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = fileUrl;
        a.download = "Resumes_" + new Date().toISOString().split("T")[0] + ".zip";
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(fileUrl);
        toast.success("Reports downloaded successfully!");
      } else if (contentType && contentType.includes("application/pdf")) {
        // If the response is a PDF file
        const blob = await response.blob();
        const fileUrl = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = fileUrl;
        a.download = "Resume_" + new Date().toISOString().split("T")[0] + ".pdf";
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(fileUrl);
        toast.success("Report downloaded successfully!");
      } else {
        throw new Error("Unknown file type.");
      }
  
    } catch (error) {
      toast.error("Failed to download reports.");
      console.error("Download error:", error);
    }
  };

  
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

  // Handle Email Reports functionality
  const handleEmailReports = async () => {
    const selectedReports = filteredReports.filter(report => report.selected);
    if (selectedReports.length === 0) {
      toast.error("No reports selected! Please select at least one.");
      return;
    }

    try {
      await Promise.all(
        selectedReports.map((report) => {
          const emailData = {
            to: report.candidateEmail,
            subject: "Selected Report",
            body: `Here is the report for ${report.name}:`,
            report: report,
          };

          return fetch("http://127.0.0.1:8000/api/sendemail/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(emailData),
          });
        })
      );

      toast.success("Emails sent successfully!");
    } catch (error) {
      toast.error("Failed to send emails.");
      console.error("Email error:", error);
    }
  };

  const handlePrint = () => {
    window.print();
  };

  // Show Confirmation Dialog
  const showConfirmationDialog = (action) => {
    setActionType(action);
    setDialogVisible(true);
  };

  // Confirm the action
  const confirmAction = () => {
    if (actionType === "delete") {
      handleDeleteReports();
    } else if (actionType === "email") {
      handleEmailReports();
    }
    setDialogVisible(false);
  };

  // Cancel the action
  const cancelAction = () => {
    setDialogVisible(false);
  };

  
  const handleReportClick = id => {
    navigate(`/summary/`); // Navigate to summary page with report ID
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
                        checked={report.selected || false}
                        onChange={e => {
                          e.stopPropagation();
                          handleSelectOne(report.id);
                        }}
                      />
                    </div>

                    <div className="name-date-column">
                      <div>
                        <strong>Job:</strong> {jobTitle ? jobTitle : report.job_id}
                      </div>
                      <div><strong>Date:</strong> {created_at || report.created_at ? new Date(report.created_at).toLocaleDateString() : "N/A"}</div>
                    </div>

                    <div className="score-column">
                      <strong>Score:</strong> {Math.min(10, ((score || report.score) / 10).toFixed(1))} / 10
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
                <button onClick={() => showConfirmationDialog("email")}>📧 Email</button>
                <button onClick={() => handleDownloadReports("download")}>📥 Download</button>
                <button onClick={() => showConfirmationDialog("delete")}>🗑️ Delete</button>
                <button onClick={() => handlePrint()}>🖨️ Print</button>
              </div>
            </>
          )}
        </>
      )}

      {/* Confirmation Dialog */}
      {dialogVisible && (
        <div className="confirmation-dialog">
          <div className="dialog-content">
            <h3>Are you sure you want to {actionType} the selected reports?</h3>
            <button onClick={confirmAction}>Yes</button>
            <button onClick={cancelAction}>No</button>
          </div>
        </div>
      )}
    </div>
  );
};

export default Reports;
