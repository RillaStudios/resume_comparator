import React, { useState, useEffect } from "react";
import "./reports.modules.css";
import { toast } from "react-toastify";
import { useLocation, useNavigate } from "react-router-dom";
import CircularScore from "./CircularScore";
 

/*
 Author: Michael Tamatey / Navjot Kaur
 Date: 20250222
 Description: This class allows users to view comparison results
*/

const Reports = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { jobTitle, score, created_at, job_id } = location.state || {};
  const [sortCriteria, setSortCriteria] = useState("score");
  const [sortOrder, setSortOrder] = useState("desc");
  const [selectAll, setSelectAll] = useState(false);
  const [filter, setFilter] = useState("all");
  const [allReports, setAllReports] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [dialogVisible, setDialogVisible] = useState(false);
  const [actionType, setActionType] = useState("");
  const [searchTerm, setSearchTerm] = useState("");


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
    const matchesFilter =
      (filter === "passed" && report.score >= 70) ||
      (filter === "failed" && report.score < 70) ||
      filter === "all";
  
    const jobTitle = String(report.job_id?.title || "").toLowerCase();
    const matchesSearch = jobTitle.includes(searchTerm.toLowerCase());
  
    return matchesFilter && matchesSearch;
  });


  // Handle Download Report functionality
  const handleDownloadReports = async (action) => {
    const selectedReports = filteredReports.filter((report) => report.selected);
    if (selectedReports.length === 0) {
      toast.error("No reports selected! Please select at least one.");
      return;
    }

    const selectedReportIds = selectedReports.map((report) => report.id);
    console.log(action, selectedReportIds);

    const report_ids = selectedReportIds.join(",");

    try {
      const res = await fetch(`http://127.0.0.1:8000/api/reports/download/?report_ids=${report_ids}`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      });

      if (!res.ok) {
        throw new Error("Failed to download reports");
      }

      const blob = await res.blob();
      const isSingleReport = selectedReports.length === 1;
      const fileName = isSingleReport ? "report.pdf" : "reports.zip";

      const link = document.createElement("a");
      link.href = window.URL.createObjectURL(blob);
      link.download = fileName;
      link.click();

      toast.success("Reports downloaded successfully!");
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
  
    
    const recipientEmail = "tamateymichael99@gmail.com";
  
    // Extract only the report IDs to send
    const reportIds = selectedReports.map(report => report.id);
  
    try {
      const response = await fetch("http://127.0.0.1:8000/api/sendselectedreports/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          report_ids: reportIds,
          email: recipientEmail,
        }),
      });
  
      const result = await response.json();
  
      if (response.ok) {
        toast.success("Reports emailed successfully!");
      } else {
        toast.error(`Failed to send: ${result.error}`);
      }
    } catch (error) {
      toast.error(`Error sending reports: ${error.message}`);
      console.error("Email error:", error);
    }
  };


  //handle print button
  const handlePrint = () => {
    const originalContent = document.body.innerHTML;
    const printContent = document.querySelector('.reports-container').outerHTML;
    document.body.innerHTML = printContent;

    window.print();

    document.body.innerHTML = originalContent;
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


   // fetch report data and navigate to summary page
const handleReportClick = async (reportId) => {
  try {
    const response = await fetch(`http://127.0.0.1:8000/api/reports/${reportId}/`, {
      method: "GET",
    });

    if (!response.ok) throw new Error("Failed to fetch report");

    const data = await response.json();

    toast.success("Fetched report successfully!");

    navigate(`/summary/${reportId}`); // navigate to summary page with report ID
  } catch (error) {
    console.error("Error:", error);
    toast.error("Failed to load report. Please try again.");
  } finally {
    setTimeout(() => {
      setLoading(false);
    }, 1000);
  }
};

  const sortedReports = [...filteredReports].sort((a, b) => {
    if (sortCriteria === "date") {
      return sortOrder === "asc"
        ? new Date(a.created_at) - new Date(b.created_at)
        : new Date(b.created_at) - new Date(a.created_at);
    } else if (sortCriteria === "score") {
      return sortOrder === "asc" ? a.score - b.score : b.score - a.score;
    } else if (sortCriteria === "job") {
      return sortOrder === "asc"
        ? String(a.job_id).localeCompare(String(b.job_id))
        : String(b.job_id).localeCompare(String(a.job_id));
    }
    return 0;
  });


  return (
    <div className="reports-container">
      <h2>All Reports</h2>

      <div className="search-container">
        <label>Search by Job Title: </label>
          <input
          type="text"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          placeholder="Enter job title..."
        />
      </div>

      <br />


      {/* Show Loading/Error */}
      {loading && <p>Loading reports...</p>}
      {error && <p className="error">{error}</p>}

      {!loading && !error && (
        <>
          <div className="filter-sort-select-container">

            {/* Select All Checkbox */}
            <div className="select-all">
              <label>
                <input type="checkbox" checked={selectAll} onChange={handleSelectAll} />
                Select All
              </label>
            </div>

            {/* Filter Dropdown */}
            <div className="filter-container">
              <label>Filter by Result: </label>
              <select value={filter} onChange={e => setFilter(e.target.value)}>
                <option value="all">All</option>
                <option value="passed">Passed</option>
                <option value="failed">Failed</option>
              </select>
            </div>

            {/* Sort Dropdown */}
            <div className="sort-container">
              <label>Sort by: </label>
              <select value={sortCriteria} onChange={(e) => setSortCriteria(e.target.value)}>
                <option value="date">Date</option>
                <option value="score">Score</option>
                <option value="job">Job Title</option>
              </select>

              <button onClick={() => setSortOrder(sortOrder === "asc" ? "desc" : "asc")}>
                {sortOrder === "asc" ? "🔼 Asc" : "🔽 Desc"}
              </button>
            </div>
          </div>
          {/* No Data Message */}
          {filteredReports.length === 0 ? (
            <p className="no-data">No information to display</p>
          ) : (
            <>
              {/* Reports List */}
              <div className="reports-list">
                {sortedReports.map(report => (
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
                        <strong>Job Title:</strong> {jobTitle ? jobTitle : report.title}
                      </div>
                      <div>
                        <strong>Job:</strong> {jobTitle ? jobTitle : report.job_id}
                      </div>
                      <div>
                        <strong>Applicant Name:</strong> {report.applicant_name || "N/A"}
                      </div>
                      <div>
                        <strong>Applicant Email:</strong> {report.applicant_email || "N/A"}
                      </div>
                      <div><strong>Date:</strong> {created_at || report.created_at ? new Date(report.created_at).toLocaleDateString() : "N/A"}</div>
                    </div>

                    {/* <div className="score-column">
                      <strong>Score:</strong> {Math.min(10, ((score || report.score) / 10).toFixed(1))} / 10
                    </div>

                    <div className="pass-fail-column">
                      <strong>{((score || report.score) / 10).toFixed(1) >= 7 ? "✅ Passed" : "❌ Failed"}</strong>
                    </div> */}
                    <div className="pass-fail-column">
                      <div className="circular-score">
                    <CircularScore score={score || report.score} />
                    </div>
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

