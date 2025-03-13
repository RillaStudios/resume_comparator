import "./mainPage.modules.css";
import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import spinner from "../../assets/image/loadingSpinner.gif";
import { toast } from "react-toastify";



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
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate();
  

  // Fetch jobs from Django backend
  useEffect(() => {
    fetch("http://127.0.0.1:8000/api/job-postings/")  // Fetch job list from backend
      .then((res) => res.json())
      .then((data) => {

        console.log("Data:", data);

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
      toast.warning("Please select a job title and upload your resume."); // message to user
       return;
    }
    setLoading(true);

    const formData = new FormData();
    formData.append("resume", uploadedFile);
    formData.append("jobId", selectedJob.id);  // Send job ID only

    try {
      const response = await fetch("http://127.0.0.1:8000/api/compare/", {
        method: "POST",
        body: formData,
      });

      console.log("Response status:", response.status);
      console.log("Response headers:", response.headers);

      if (!response.ok) throw new Error("Failed to compare resume.");

      const data = await response.json();

      console.log("Data:", data);

      toast.success("Comparing successful!"); // ✅ Show success only after a successful response

    } catch (error) {
      console.error("Error comparing resume:", error);
      toast.error("Comparison failed. Please try again."); // ❌ Show error if request fails
    }finally{
      setTimeout(() => {
        setLoading(false);
      }, 1000);
    }
  };

  return (
    <div className="main-container">

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
             <p><strong>Company:</strong> {selectedJob.company.name}</p>
              <p><strong>Location:</strong> {selectedJob.location.city}, {selectedJob.location.province}, {selectedJob.location.country}</p>
              <p><strong>Description:</strong> {selectedJob.company.description}</p>
              <p><strong>Summary:</strong> {selectedJob.job_description.summary}</p>
              <p><strong>Responsibilities:</strong></p>
              <ol>
                {selectedJob.job_description.responsibilities.map((resp, index) => (
                  <li key={index}>{resp}</li>
                ))}
              </ol>
              <p><strong>Must-Have Requirements:</strong></p>
              <ol>
                {selectedJob.job_description.requirements.must_have.map((req, index) => (
                  <li key={index}>{req}</li>
                ))}
              </ol>
              <p><strong>Nice-to-Have Requirements:</strong></p>
              <ol>
                {selectedJob.job_description.requirements.nice_to_have.map((req, index) => (
                  <li key={index}>{req}</li>
                ))}
              </ol>
              <p><strong>Salary:</strong> {selectedJob.salary.currency} {selectedJob.salary.min} - {selectedJob.salary.max} per {selectedJob.salary.period}</p>
              <p><strong>Employment Type:</strong> {selectedJob.employment_type}</p>
              <p><strong>Benefits:</strong></p>
              <ol>
                {selectedJob.benefits.map((benefit, index) => (
                  <li key={index}>{benefit}</li>
                ))}
              </ol>
              <p><strong>Posted Date:</strong> {selectedJob.posted_date}</p>
              <p><strong>Application Deadline:</strong> {selectedJob.application_deadline}</p>
              <p><strong>Contact Email:</strong> <a href={'mailto:${selectedJob.contact_email}'}>{selectedJob.contact_email}</a></p>
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
      {/* Compare Button - Disabled until a resume is uploaded */}
      <button 
  className="convert-button" 
  onClick={handleCompare} 
  disabled={!uploadedFile || loading}
  title={!uploadedFile ? "Please upload a file first!" : ""}
>
  {loading ? "Processing..." : "Compare"}
</button>

      {loading && (
        <div className="loading-spin">
          <div className="loading-spinner">
            <img src={spinner} alt="Loading..." />
          </div>
        </div>
      )}
      
  </div>
    
  );
};

export default MainPage;