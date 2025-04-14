import './jobSearch.css';
import React, { useState, useEffect } from 'react';
import axios from 'axios';

const JobSearch = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [jobList, setJobList] = useState([]);
  const [loading, setLoading] = useState(false);

  const fetchJobs = async (query = '') => {
    try {
      setLoading(true);
      const response = await axios.get(`http://127.0.0.1:8000/job-postings/`, {
        params: {
          search: query
        }
      });
      setJobList(response.data);
    } catch (err) {
      console.error('Error fetching jobs:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchJobs(); // fetch all jobs on first load
  }, []);

  const handleSearch = (e) => {
    e.preventDefault();
    fetchJobs(searchTerm);
  };

  return (
    <div>
<form onSubmit={handleSearch} className="search-form">
  <label className="search-label">Filter by Job: </label>
  <input
    type="text"
    placeholder="Search job postings..."
    value={searchTerm}
    onChange={(e) => setSearchTerm(e.target.value)}
    className="search"
  />
  <button type="submit" className="search-button">
    Search
  </button>
</form>



      {loading ? (
        <p>Loading jobs...</p>
      ) : (
        <ul>
          {jobList.map((job) => (
            <li key={report.job_id}>
              <h2>{job.title}</h2>
              <p>{job.description}</p>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default JobSearch;
