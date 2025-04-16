import React, { useEffect, useState } from "react";
import "./summary.modules.css";
import { toast } from "react-toastify";
import { useParams } from 'react-router-dom';
import axios from 'axios';
import BackButton from '../../common/backButton'; 

const Summary = () => {
  const { id } = useParams(); 
  const [reportData, setReportData] = useState(null);

  useEffect(() => {
    const fetchReportData = async () => {
      try {
        const response = await axios.get(`http://127.0.0.1:8000/api/reports/${id}`);
        setReportData(response.data);
      } catch (error) {
        toast.error("Failed to fetch report data");
        console.error(error);
      }
    };

    fetchReportData();
  }, [id]);



  // Handle Email Reports functionality
  const handleEmailReports = async () => {
    // Check if necessary data is available
    const { applicant_name, applicant_email, job_id } = reportData;
  
    if (!applicant_name || !applicant_email || !job_id) {
      toast.error("Missing required candidate information.");
      return;
    }
  
    try {
      // Send the email using the candidate's data
      const response = await fetch("http://127.0.0.1:8000/api/sendemail/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          applicant_name,
          applicant_email,
          job_id,
        }),
      });
  
      // Check if the email was sent successfully
      if (response.ok) {
        toast.success("Email sent successfully!");
      } else {
        throw new Error("Failed to send email");
      }
    } catch (error) {
      toast.error(`Error sending email: ${error.message}`);
      console.error("Email error:", error);
    }
  };

  // Function to print 
  const handlePrint = () => {
    const printContent = document.querySelector('.candidate-summary-container').outerHTML;
    const printWindow = window.open('', '_blank');
    printWindow.document.write(`
      <html>
        <head>
          <title>Candidate Summary</title>
          <link rel="stylesheet" href="summary.modules.css" />
        </head>
        <body>${printContent}</body>
      </html>
    `);
    printWindow.document.close();
    printWindow.print();
  };

  if (!reportData) return <div>Loading report...</div>;

  const maxLength = Math.max(
    reportData.passing?.length || 0,
    reportData.failing?.length || 0
  );

  return (
    <div className="candidate-summary-container">
      <BackButton />
      <h1 className="candidate-summary-title">Candidate Summary</h1>
      <div className="candidate-summary-title">
      <p><strong>Name:</strong> {reportData.applicant_name}</p>
      <p><strong>Email:</strong> {reportData.applicant_email}</p>
      <p><strong>Job ID:</strong> {reportData.job_id}</p>
      <p><strong>Score Status:</strong> {((reportData.score) / 10).toFixed(1) >= 7 ? "✅ Passed" : "❌ Failed"}</p> 

      </div>

      <section className="candidate-summary-section">
        <h2 className="summary-section-title">Overall Recommendation</h2>
        <p><strong>Summary:</strong> {reportData.report_text}</p>

        <br />
        <br />

        <h2 className="summary-section-title">Passed & Failed Criteria</h2>
        <table className="candidate-summary-table">
          <thead>
            <tr>
              <th>✅ Passed</th>
              <th>❌ Failed</th>
            </tr>
          </thead>
          <tbody>
            {Array.from({ length: maxLength }).map((_, index) => (
              <tr key={index}>
                <td>
                  {reportData.passing?.[index] &&
                    Object.entries(reportData.passing[index]).map(([stage, info]) => (
                      <div key={stage}>
                        <strong>{stage}</strong>: {info.description}
                      </div>
                    ))}
                </td>
                <td>
                  {reportData.failing?.[index] &&
                    Object.entries(reportData.failing[index]).map(([stage, info]) => (
                      <div key={stage}>
                        <strong>{stage}</strong>: {info.description}
                      </div>
                    ))}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>

      <section className="candidate-summary-section">
        
      </section>

      <div className="candidate-action-buttons">
        <button className="candidate-btn print-btn" onClick={handlePrint}>🖨️ Print</button>
        <button className="candidate-btn email-btn" onClick={handleEmailReports}>📧 Email Candidate</button>
      </div>
    </div>
  );
};

export default Summary;