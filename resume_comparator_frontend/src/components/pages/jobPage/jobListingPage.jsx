import React, { useState, useEffect } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import "./JobListingPage.css";
 import BackButton from "../../common/backButton";


 /*
 Author: Navjot Kaur
 Date: 20250222
 Description: This component displays a list of job postings. It allows users to search for job postings by title, edit existing postings, and delete postings. 
 The component fetches data from an API and handles loading and error states.
 It also includes a confirmation dialog for deletion actions.
*/
const JobListingPage = () => {
  const [jobPostings, setJobPostings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState("");
  const [dialogVisible, setDialogVisible] = useState(false);
  const [jobToDelete, setJobToDelete] = useState(null);


  const navigate = useNavigate();

  // Fetch job postings
  useEffect(() => {
    axios.get("http://localhost:8000/api/job-postings/")
      .then((response) => {
        setJobPostings(response.data);
        setLoading(false);
      })
      .catch(() => {
        setError("Failed to fetch job postings");
        setLoading(false);
      });
  }, []);

  const confirmAction = () => {
    handleDeleteJob(jobToDelete);
    setDialogVisible(false);
  };
  
  const cancelAction = () => {
    setDialogVisible(false);
    setJobToDelete(null);
  };
  
  const handleDeleteClick = (jobId) => {
    setJobToDelete(jobId);
    setDialogVisible(true);
  };
  
  const handleDeleteJob = (jobId) => {
    axios.delete("http://localhost:8000/api/job-postings/", { data: { id: jobId } })
      .then(() => {
        setJobPostings(jobPostings.filter((job) => job.id !== jobId));
      })
      .catch(() => {
        setError("Failed to delete job posting");
      });
  };

    // Filter reports based on user selection
    const filteredJobs = jobPostings.filter(job => {
    
      const jobTitle = String(job.title || "").toLowerCase();
      const matchesSearch = jobTitle.includes(searchTerm.toLowerCase());
    
      return matchesSearch;
    });

  const handleEditJob = (jobId) => {
    navigate(`/update-job/${jobId}`);
  };

  const handleAddJob = () => {
    navigate("/create-job");
  };

  if (loading) return <div>Loading...</div>;
  if (error) return <div>{error}</div>;

  return (
    <div>
      <BackButton />
      <h1>Job Postings</h1>

      <div className="search-container">
        <label>Search by Job Title: </label>
          <input
          type="text"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          placeholder="Enter job title..."
        />
      </div>
      <div className="job-container">
        {filteredJobs.map((job) => (
          <div key={job.id} className="job-card">
            <div className="job-info">
              <h3 className="title">{job.title}</h3>
              <p className="company">{job.company_name}</p>
              <p className="location">📍{job.city}, {job.prov_state}</p>
              <p className="badge">{job.employment_type}</p>
              <p className="posting-date">🕒 {new Date(job.posting_date).toLocaleDateString('en-US', {
                year: 'numeric',
                month: 'long',
                day: 'numeric'
              })}</p>
            </div>
            <div className="job-actions">
              <button className="edit-btn" onClick={() => handleEditJob(job.id)}>Edit</button>
              <button className="delete-btn" onClick={() => handleDeleteClick(job.id)}>Delete</button>
              </div>
          </div>
        ))}

        {/* Add Job Card */}
        <div className="add-job-card" onClick={handleAddJob}>
          +
        </div>
      </div>
      {/* Confirmation Dialog */}
      {dialogVisible && (
  <div className="confirmation-dialog">
    <div className="dialog-content">
      <h3>Are you sure you want to delete this job posting?</h3>
      <button onClick={confirmAction}>Yes</button>
      <button onClick={cancelAction}>No</button>
    </div>
  </div>
    )}
    </div>
  );
};

export default JobListingPage;
