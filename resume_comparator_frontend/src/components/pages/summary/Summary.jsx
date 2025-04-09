import React, { useEffect, useState } from "react";
import "./summary.modules.css";
import { toast } from "react-toastify";
import { useParams } from 'react-router-dom';
import axios from 'axios';

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

  return (
    <div className="candidate-summary-container">
      <h1 className="candidate-summary-title">Candidate Summary</h1>
      
      <p><strong>Name:</strong> {reportData.applicant_name}</p>
      <p><strong>Email:</strong> {reportData.applicant_email}</p>
      <p><strong>Job ID:</strong> {reportData.job_id}</p>
      <p><strong>Score:</strong> {reportData.score}</p>

      <section className="candidate-summary-section">
        <h2 className="summary-section-title">Overall Recommendation</h2>
        <p><strong>Summary:</strong> {reportData.report_text}</p>
      </section>

      <section className="candidate-summary-section">
        <h2 className="summary-section-title">Passed & Failed Criteria</h2>
        <table className="candidate-summary-table">
          <thead>
            <tr>
              <th>✅ Passed</th>
              <th>❌ Failed</th>
            </tr>
          </thead>
          
          
        </table>
      </section>

      <div className="candidate-action-buttons">
        <button className="candidate-btn print-btn" onClick={handlePrint}>🖨️ Print</button>
      </div>
    </div>
  );
};

export default Summary;