import "./mainPage.modules.css";
import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import jobs from "./jobs.json";

/*
 Author: Michael Tamatey/ Navjot Kaur
 Date: 20250222
 Description: This class allows users to select job posting and upload resumes to compare 
*/

export const MainPage = () => {
  // const [userDetails, setUserDetails] = useState(null); // Store user details
  const [jobs, setJobs] = useState([]);  // Store jobs from backend
  const [selectedJob, setSelectedJob] = useState(null); // Store selected job
  const [uploadedFile, setUploadedFile] = useState(null);
  const [fileName, setFileName] = useState("");
  const navigate = useNavigate();

 // Fetch jobs from Django backend
 useEffect(() => {
  fetch("http://127.0.0.1:8000/api/jobs/")  // Fetch job list from backend
    .then((res) => res.json())
    .then((data) => {
      setJobs(data);
      setSelectedJob(data[0]);  // Default to first job
    })
    .catch((err) => console.error("Error fetching jobs:", err));
}, []);

   // Handle job selection
   const handleJobChange = (event) => {
    const selectedTitle = event.target.value;
    const job = jobs.find((job) => job.title === selectedTitle);
    setSelectedJob(job);
  };

  // Handle file upload
  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      setUploadedFile(file);
      setFileName(file.name);
    }
  };

  // Send resume to backend for processing
  const handleCompare = async () => {
    if (!selectedJob || !uploadedFile) {
      alert("Please select a job title and upload your resume.");
      return;
    }

    const formData = new FormData();
    formData.append("resume", uploadedFile);
    formData.append("jobId", selectedJob.id);  // Send job ID only

    try {
      const response = await fetch("http://127.0.0.1:8000/api/compare/", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) throw new Error("Failed to compare resume.");

      const data = await response.json();

      navigate("/reports", { state: { jobTitle: selectedJob.title, result, score: data.matchScore } });

    } catch (error) {
      console.error("Error comparing resume:", error);
      alert("Error processing resume.");
    }
  };

  return (
    <div className="main-container">
      <h3 className="user-d">Welcome User !!</h3> 

      <div className="container-body">
        <div className="left-section">
          {/* Job Selection Dropdown */}
          <div className="dropdown-container">
            <label htmlFor="job-select">Select a Job:</label>
            <select id="job-select" onChange={handleJobChange}>
              {jobs.map((job) => (
                <option key={job.id} value={job.title}>{job.title}</option>
              ))}
            </select>
          </div>

          {/* Job Description */}
          {selectedJob && (
            <div className="display-box">
              <p>Company: {selectedJob.company}</p>
              <p>Description: {selectedJob.description}</p>
            </div>
          )}
        </div>

        

        {/* Resume Upload */}
        <div className="upload-container">
          <label htmlFor="file-upload">Upload Resume:</label>
          <input type="file" id="file-upload" onChange={handleFileUpload} />
          {uploadedFile && (
                <div className="uploaded-file">
                  <p>Uploaded File: {fileName}</p>
                </div>
              )}
            </div>
          </div>

      {/* Compare Button */}
      <button className="convert-button" onClick={handleCompare}>Compare</button>
    </div>
  );
};

export default MainPage;