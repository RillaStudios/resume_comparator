import "./mainPage.modules.css";
import React, { useEffect, useState, useRef } from "react";
import { useNavigate } from "react-router-dom";
import spinner from "../../assets/image/loadingSpinner.gif";
import { toast } from "react-toastify";
import ReportGraph from "./reportGraph/reportGraph";
import BackButton from '../common/backButton'; 
/*
 Author: Michael Tamatey / Navjot Kaur
 Date: 20250222
 Description: This class allows users to select job posting and upload resumes to compare 
*/

export const MainPage = () => {
  const [jobs, setJobs] = useState([]);
  const [selectedJob, setSelectedJob] = useState(null);
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const fileInputRef = useRef(null); // Ref to the file input element
  const [fileInputKey, setFileInputKey] = useState(Date.now());

  // Fetch jobs from Django backend
  useEffect(() => {
    fetch("http://127.0.0.1:8000/api/job-postings/")
      .then((res) => res.json())
      .then((data) => {
        console.log("Data:", data);
        setJobs(data);
        setSelectedJob(data[0]); // Set the first job as the selected job by default
      })
      .catch((err) => console.error("Error fetching jobs:", err));
  }, []);

  // Handle job selection
  const handleJobChange = (event) => {
    const selectedTitle = event.target.value;
    const job = jobs.find((job) => job.title === selectedTitle);
    setSelectedJob(job);
  };

  const clearFiles = () => {
    setUploadedFiles([]);
    if (fileInputRef.current) {
      fileInputRef.current.value = null;
    }
    setFileInputKey(Date.now()); // Reset the key to force re-render of the input
  };

  // Handle file upload - now appending files without duplicates
  const handleFileUpload = (event) => {
    const files = Array.from(event.target.files);
    setUploadedFiles((prevFiles) => {
      const newFiles = files.filter(
        (file) => !prevFiles.some((prev) => prev.name === file.name)
      );
      return [...prevFiles, ...newFiles];
    });
  };

  // Send resume to backend for processing
  const handleCompare = async () => {
    if (!selectedJob || uploadedFiles.length === 0) {
      toast.warning("Please select a job title and upload your resume.");
      return;
    }
    setLoading(true);

    const formData = new FormData();
    uploadedFiles.forEach((file) => {
      formData.append("resume", file);
    });
    formData.append("jobId", selectedJob.id);

    try {
      const response = await fetch("http://127.0.0.1:8000/api/compare/", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) throw new Error("Failed to compare resume.");

      const data = await response.json();

      toast.success("Comparing successful!");

      navigate("/singlereports", {
        state: {
          jobTitle: selectedJob.title,
          reports: Array.isArray(data) ? data : [data],
        },
      });
    } catch (error) {
      console.error("Error comparing resume:", error);
      toast.error("Comparison failed. Please try again.");
    } finally {
      setTimeout(() => {
        setLoading(false);
      }, 1000);
    }
  };

  // Function to parse text into a list based on new line or comma
  const parseTextToList = (text) => {
    if (!text) return [];
    return text.includes('\n') ? text.split('\n') : text.split(',');
  };

  const handleAddJob = () => {
    navigate("/create-job");
  };

  return (

    <> 
    <BackButton />
    <div className="main-container">

      {/* Add Job Card */}
    <div className="add-job-card-main" onClick={handleAddJob}>
          Add Job
      </div>



    <div className="graphs-container">
    <div>
        <ReportGraph />
    </div>
    </div>

      <div className="container-body">
        <div className="left-section">
          {/* Job Selection Dropdown */}
          <div className="dropdown-container">
            <label htmlFor="job-select">Select a Job:</label>
            <select id="job-select" onChange={handleJobChange}>
              {jobs.map((job) => (
                <option key={job.id} value={job.title}>
                  {job.title}
                </option>
              ))}
            </select>
          </div>

          {/* Job Description */}
          {selectedJob && (
  <div className="display-box">
    <p><strong>Company:</strong> {selectedJob.company_name}</p>
    <p><strong>Location:</strong> {selectedJob.city}, {selectedJob.prov_state}, {selectedJob.country}</p>
    <p><strong>Description:</strong> {selectedJob.company_desc}</p>
    <p><strong>Summary:</strong> {selectedJob.summary}</p>

    <p><strong>Responsibilities:</strong></p>
    <ul>
      {parseTextToList(selectedJob.responsibilities).map((item, index) => (
        <li key={index}>{item.trim()}</li>
      ))}
    </ul>

    <p><strong>Must-Have Requirements:</strong></p>
    <ul>
      {parseTextToList(selectedJob.skills_qual_required).map((item, index) => (
        <li key={index}>{item.trim()}</li>
      ))}
    </ul>

    <p><strong>Nice-to-Have Requirements:</strong></p>
    <ul>
      {parseTextToList(selectedJob.skills_qual_nice_to_have).map((item, index) => (
        <li key={index}>{item.trim()}</li>
      ))}
    </ul>
    <p><strong>Education Required:</strong></p>
    <ul>
      {parseTextToList(selectedJob.education_required).map((item, index) => (
        <li key={index}>{item.trim()}</li>
      ))}
    </ul>
    <p><strong>Experience Required:</strong></p>
    <ul>
      {parseTextToList(selectedJob.experience_required).map((item, index) => (
        <li key={index}>{item.trim()}</li>
      ))}
    </ul>

    <p><strong>Salary:</strong> {selectedJob.salary_currency_type} {selectedJob.salary_min} - {selectedJob.salary_max} per {selectedJob.salary_interval}</p>
    <p><strong>Employment Type:</strong> {selectedJob.employment_type}</p>

    <p><strong>Benefits:</strong></p>
    <ul>
      {parseTextToList(selectedJob.benefits).map((item, index) => (
        <li key={index}>{item.trim()}</li>
      ))}
    </ul>

    <p><strong>Posted Date:</strong> {selectedJob.posting_date}</p>
    <p><strong>Application Deadline:</strong> {selectedJob.closing_date}</p>
    <p><strong>Contact Email:</strong> <a href={`mailto:${selectedJob.contact_email}`}>{selectedJob.contact_email}</a></p>
  </div>
)}
        </div>

        {/* Resume Upload */}
        <div className="upload-container">
          <label htmlFor="file-upload">Upload Resume:</label>
          <input
            key={fileInputKey}
            type="file"
            id="file-upload"
            multiple
            onChange={handleFileUpload}
            ref={fileInputRef}
          />
          {uploadedFiles.length > 0 && (
            <div className="uploaded-file">
              <p>Uploaded Files:</p>
              <ol>
                {uploadedFiles.map((file, index) => (
                  <li key={index}>{file.name}</li>
                ))}
              </ol>
              {/* Clear All Files Button */}
              <button
                className="clear-button"
                onClick={clearFiles}
                disabled={loading}
              >
                Clear All Files
              </button>
            </div>
          )}
        </div>
      </div>

      {/* Compare Button */}
      <button
        className={`convert-button ${loading ? "processing" : ""}`}
        onClick={handleCompare}
        disabled={uploadedFiles.length === 0 || loading}
        title={uploadedFiles.length === 0 ? "Please upload at least one file!" : ""}
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

    </>
  );
};

export default MainPage;