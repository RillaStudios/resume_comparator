import "./reports.modules.css";
import { useLocation, useNavigate } from "react-router-dom";

/*
 Author: Michael Tamatey
 Date: 20250222
 Description: This class allows users to view single comparison results
*/

const SingleReports = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { jobTitle, reports = [] } = location.state || {};

  const handleReportClick = (id) => {
    navigate(`/summary/`);
  };

  return (
    <div className="reports-container">
      <h2>Single Report Results</h2>
      <h4>Click on Reports Page for summary</h4>

      {/* Reports List */}
      <div className="reports-list">
        {reports.map((report, index) => (
          <div className="report-item" key={index}>
            <div className="name-date-column">
              <div>
                <strong>Job Title:</strong> {jobTitle || "N/A"}
              </div>
              <div>
                <strong>Job ID:</strong> {report.job_id || "N/A"}
              </div>
              <div>
                <strong>Applicant Name:</strong> {report.applicant_name || "N/A"}
              </div>
              <div>
                <strong>Applicant Email:</strong> {report.applicant_email || "N/A"}
              </div>
              <div>
                <strong>Date:</strong>{" "}
                {report.created_at
                  ? new Date(report.created_at).toLocaleDateString()
                  : "N/A"}
              </div>
            </div>

            <div className="score-column">
              <strong>Score:</strong> {(report.score / 10).toFixed(1)} / 10
            </div>

            <div className="pass-fail-column">
              <strong>{(report.score / 10) >= 7.5 ? "✅ Passed" : "❌ Failed"}</strong>
            </div>

            <div className="view-column">
              <button onClick={() => handleReportClick(report.id)}>📝</button>
            </div>
          </div>
        ))}
      </div>

      <a href="/" className="compare-again">
        Click here to compare again
      </a>
      <a href="/reports" className="compare-again">
        Click here to view all reports
      </a>
    </div>
  );
};

export default SingleReports;
