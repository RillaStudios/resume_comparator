import React, { useEffect,useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

const CreateJobPage = () => {
  const navigate = useNavigate();

  // States for all fields
  const [title, setTitle] = useState("");
  const [companyName, setCompanyName] = useState("");
  const [companyDesc, setCompanyDesc] = useState("");
  const [summary, setSummary] = useState("");
  const [responsibilities, setResponsibilities] = useState("");
  const [skillsRequired, setSkillsRequired] = useState("");
  const [skillsNiceToHave, setSkillsNiceToHave] = useState("");
  const [address, setAddress] = useState("");
  const [city, setCity] = useState("");
  const [province, setProvince] = useState("");
  const [country, setCountry] = useState("");
  const [zipCode, setZipCode] = useState("");
  const [remote, setRemote] = useState(false);
  const [salaryMin, setSalaryMin] = useState("");
  const [salaryMax, setSalaryMax] = useState("");
  const [salaryCurrency, setSalaryCurrency] = useState("");
  const [salaryInterval, setSalaryInterval] = useState("");
  const [employmentType, setEmploymentType] = useState("");
  const [benefits, setBenefits] = useState("");
  const [postingDate, setPostingDate] = useState("");
  const [closingDate, setClosingDate] = useState("");
  const [contactName, setContactName] = useState("");
  const [contactEmail, setContactEmail] = useState("");
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);

    const countryStateMap = {
      Canada: [
        "Alberta", "British Columbia", "Manitoba", "New Brunswick",
        "Newfoundland and Labrador", "Nova Scotia", "Ontario", "Prince Edward Island",
        "Quebec", "Saskatchewan"
      ],
      USA: [
        "Alabama", "Alaska", "Arizona", "California", "Florida", "New York", "Texas", "Washington"
      ],
      India: [
        "Andhra Pradesh", "Delhi", "Gujarat", "Karnataka", "Maharashtra", "Punjab", "Rajasthan", "Tamil Nadu"
      ]
    };
    
    const [availableProvinces, setAvailableProvinces] = useState([]);
    
    useEffect(() => {
      if (country && countryStateMap[country]) {
        setAvailableProvinces(countryStateMap[country]);
        setProvince(""); // Reset province when country changes
      } else {
        setAvailableProvinces([]);
      }
    }, [country]);
      
    
  const handleSubmit = (e) => {
    e.preventDefault();

 
    const jobData = {
      title: title,
      company_name: companyName,
      company_desc: companyDesc,
      summary: summary,
      responsibilities: responsibilities,
      skills_qual_required: skillsRequired,
      skills_qual_nice_to_have: skillsNiceToHave,
      address: address,
      city: city,
      prov_state: province,
      country: country,
      zip_postal_code: zipCode,
      remote: remote,
      salary_min: salaryMin,
      salary_max: salaryMax,
      salary_currency_type: salaryCurrency,
      salary_interval: salaryInterval,
      employment_type: employmentType,
      benefits: benefits,
      posting_date: postingDate,
      closing_date: closingDate,
      contact_name: contactName,
      contact_email: contactEmail,
    };
    axios
      .post("http://localhost:8000/api/job-postings/", jobData)
      .then((response) => {
        setSuccess("Job posted successfully!");
        setTimeout(() => {
          navigate("/job-postings");
        }, 1000);
      })
      .catch((err) => {
        setError("Failed to post the job. Please try again.");
      });
  };

  return (
    <div>
      <h1>Create Job Posting</h1>
      {success && <div className="success-message">{success}</div>}
      {error && <div className="error-message">{error}</div>}

      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="title">Job Title</label>
          <input
            type="text"
            id="title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            required
          />
        </div>
        <div>
          <label htmlFor="companyName">Company Name</label>
          <input
            type="text"
            id="companyName"
            value={companyName}
            onChange={(e) => setCompanyName(e.target.value)}
            required
          />
        </div>
        <div>
          <label htmlFor="companyDesc">Company Description</label>
          <textarea
            id="companyDesc"
            value={companyDesc}
            onChange={(e) => setCompanyDesc(e.target.value)}
          ></textarea>
        </div>
        <div>
          <label htmlFor="jobSummary">Job Summary</label>
          <textarea
            id="jobSummary"
            value={summary}
            onChange={(e) => setSummary(e.target.value)}
            required
          ></textarea>
        </div>
        <div>
          <label htmlFor="jobResponsibilities">Job Responsibilities</label>
          <textarea
            id="jobResponsibilities"
            value={responsibilities}
            onChange={(e) => setResponsibilities(e.target.value)}
          ></textarea>
        </div>
        <div>
          <label htmlFor="jobRequirementsMustHave">Must Have Requirements</label>
          <textarea
            id="jobRequirementsMustHave"
            value={skillsRequired}
            onChange={(e) => setSkillsRequired(e.target.value)}
          ></textarea>
        </div>
        <div>
          <label htmlFor="jobRequirementsNiceToHave">Nice to Have Requirements</label>
          <textarea
            id="jobRequirementsNiceToHave"
            value={skillsNiceToHave}
            onChange={(e) => setSkillsNiceToHave(e.target.value)}
          ></textarea>
        </div>
       <div>
          <label htmlFor="jobCity">Address</label>
          <input
            type="text"
            id="jobCity"
            value={address}
            onChange={(e) => setAddress(e.target.value)}
            required
          />
        </div>
        <div>
          <label htmlFor="jobCity">City</label>
          <input
            type="text"
            id="jobCity"
            value={city}
            onChange={(e) => setCity(e.target.value)}
            required
          />
        </div>
        <div>
        <label htmlFor="jobProvince">Province/State</label>
          <select
           id="jobProvince"
           value={province}
           onChange={(e) => setProvince(e.target.value)}
           required
           disabled={!availableProvinces.length}
          >
         <option value="">Select Province/State</option>
           {availableProvinces.map((prov) => (
           <option key={prov} value={prov}>
             {prov}
            </option>
          ))}
         </select>
        </div>
        <div>
      <label htmlFor="jobCountry">Country</label>
       <select
         id="jobCountry"
        value={country}
        onChange={(e) => setCountry(e.target.value)}
        required
       >
       <option value="">Select Country</option>
       <option value="Canada">Canada</option>
       <option value="USA">USA</option>
       <option value="India">India</option>
     </select>
    </div>
        <div>
          <label htmlFor="jobRemote">Remote</label>
          <input
            type="checkbox"
            id="jobRemote"
            checked={remote}
            onChange={(e) => setRemote(e.target.checked)}
          />
        </div>
        <div>
          <label htmlFor="jobSalaryMin">Minimum Salary</label>
          <input
            type="number"
            id="jobSalaryMin"
            value={salaryMin}
            onChange={(e) => setSalaryMin(e.target.value)}
          />
        </div>
        <div>
          <label htmlFor="jobSalaryMax">Maximum Salary</label>
          <input
            type="number"
            id="jobSalaryMax"
            value={salaryMax}
            onChange={(e) => setSalaryMax(e.target.value)}
          />
        </div>
        <div>
          <label htmlFor="jobSalaryCurrency">Salary Currency</label>
            <select
             id="jobSalaryCurrency"
             value={salaryCurrency}
              onChange={(e) => setSalaryCurrency(e.target.value)}
            required
            >
           <option value="">Select Currency</option>
           <option value="CAD">CAD</option>
           <option value="USD">USD</option>
           <option value="EUR">EUR</option>
          <option value="INR">INR</option>
          </select>
        </div>

        <div>
        <label htmlFor="jobSalaryInterval">Salary Interval</label>
          <select
             id="jobSalaryInterval"
             value={salaryInterval}
             onChange={(e) => setSalaryInterval(e.target.value)}
             required
            >
            <option value="">Select Interval</option>
            <option value="hour">Hourly</option>
            <option value="day">Daily</option>
            <option value="week">Weekly</option>
            <option value="month">Monthly</option>
            <option value="year">Yearly</option>
        </select>
        </div>

        <div>
      <label htmlFor="jobEmploymentType">Employment Type</label>
        <select
         id="jobEmploymentType"
         value={employmentType}
         onChange={(e) => setEmploymentType(e.target.value)}
         required
        >
         <option value="">Select Type</option>
         <option value="Full-Time">Full-Time</option>
         <option value="Part-Time">Part-Time</option>
         <option value="Internship">Internship</option>
         <option value="Contract">Contract</option>
         <option value="Temporary">Temporary</option>
         </select>
        </div>

        <div>
          <label htmlFor="jobBenefits">Benefits</label>
          <textarea
            id="jobBenefits"
            value={benefits}
            onChange={(e) => setBenefits(e.target.value)}
          ></textarea>
        </div>
        <div>
        <label htmlFor="jobPostingDate">Posting Date</label>
        <input
          type="date"
          id="jobPostingDate"
          value={postingDate}
          onChange={(e) => setPostingDate(e.target.value)}
        />
        </div>
        <div>
          <label htmlFor="jobClosingDate">Closing Date</label>
          <input
            type="date"
            id="jobClosingDate"
            value={closingDate}
            onChange={(e) => setClosingDate(e.target.value)}
          />
        </div>
        <div>
          <label htmlFor="title">Contact Name</label>
          <input
            type="text"
            id="text"
            value={contactName}
            onChange={(e) => setContactName(e.target.value)}
          />
        </div>
        <div>
          <label htmlFor="jobContactEmail">Contact Email</label>
          <input
            type="email"
            id="jobContactEmail"
            value={contactEmail}
            onChange={(e) => setContactEmail(e.target.value)}
          />
        </div>
        <button type="submit">Create Job</button>
      </form>
    </div>
  );
};

export default CreateJobPage;
