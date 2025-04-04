import "./reports.modules.css";
import { useLocation, useNavigate } from "react-router-dom";


/*
 Author: Michael Tamatey
 Date: 20250222
 Description: This class allows users to view single comparison results
*/

const SingleReports = () => {
  const location = useLocation();
  const { jobTitle, score, date, jobId } = location.state || {};

  return (
    <div className="reports-container">
      <h2>Single Report Results</h2>
      <h4>Click on Reports Page for summary</h4>

      {/* Reports List */}
      <div className="reports-list">
                
                <div className="report-item">
                    <div className="name-date-column">
                      <div>
                      <strong>Job Title:</strong> {jobTitle || "N/A"}
                      </div>
                        <div>
                            <strong>Job ID:</strong> {jobId || "N/A"}
                        </div>
                      <div>
                        <strong>Date:</strong> {date ? new Date(date).toLocaleDateString() : "N/A"}
                    </div>
                    </div>

                    <div className="score-column">
                      <strong>Score:</strong> {Math.min(10, ((score) / 10).toFixed(1))} / 10
                    </div>

                    <div className="pass-fail-column">
                      <strong>{score >= 7 ? "✅ Passed" : "❌ Failed"}</strong>
                    </div>
                  </div>                
              </div>
    </div>
  );
};

export default SingleReports;