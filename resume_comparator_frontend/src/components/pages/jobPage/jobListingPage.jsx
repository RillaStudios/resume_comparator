import React, { useState, useEffect } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import "./JobListingPage.css";
 import BackButton from "../../common/backButton";

const JobListingPage = () => {
  const [jobPostings, setJobPostings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
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

  const handleDeleteJob = (jobId) => {
    axios.delete("http://localhost:8000/api/job-postings/", { data: { id: jobId } })
      .then(() => {
        setJobPostings(jobPostings.filter((job) => job.id !== jobId));
      })
      .catch(() => {
        setError("Failed to delete job posting");
      });
  };

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
      <div className="job-container">
        {jobPostings.map((job) => (
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
              <button className="delete-btn" onClick={() => handleDeleteJob(job.id)}>Delete</button>
            </div>
          </div>
        ))}

        {/* Add Job Card */}
        <div className="add-job-card" onClick={handleAddJob}>
          +
        </div>
      </div>
    </div>
  );
};

export default JobListingPage;
