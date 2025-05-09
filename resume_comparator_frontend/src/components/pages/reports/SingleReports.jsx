import "./reports.modules.css";
import { useLocation, useNavigate } from "react-router-dom";
import CircularScore from "./CircularScore"; 
import BackButton from "../../common/backButton";
import { toast } from "react-toastify";


/*
 Author: Michael Tamatey
 Date: 20250222
 Description: This class allows users to view single comparison results
*/

const SingleReports = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const {  score, created_at, job_id } = location.state || {};
  const { jobTitle, reports = [] } = location.state || {};

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

  return (
    
    <div className="reports-container">
      <BackButton />
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
