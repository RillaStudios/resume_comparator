import React from "react";
import "./summary.modules.css";
import { toast } from "react-toastify";


const Summary = () => {
  // Hardcoded data
  const summaryData = {

    jobRequirements: [
      { requirement: "Java, J2EE, Spring MVC, Spring Boot", score: 2, comments: "Candidate lists Java (13) but does not mention Spring MVC or Spring Boot experience." },
      { requirement: "Frontend (Angular 8+, ReactJS, VueJS, Typescript)", score: 2, comments: "Only mentions AngularJS, but no mention of modern Angular 8+, ReactJS, or VueJS." },
      { requirement: "Web UI (HTML5, CSS3, JavaScript, REST API)", score: 5, comments: "Candidate has experience with HTML, CSS, JavaScript, but no details on REST API development." },
      { requirement: "Microservices & API Development", score: 2, comments: "No explicit mention of microservices or API development experience." },
      { requirement: "Database (Oracle, Kafka, NoSQL, PostgreSQL)", score: 5, comments: "Lists Oracle, NoSQL, PostgreSQL, but no mention of Kafka experience." },
      { requirement: "AWS (EC2/EKS) or Cloud Computing", score: 6, comments: "Experience with AWS services, including EC2, Lambda, and S3, but no specific mention of EKS." },
      { requirement: "DevOps, CI/CD (Maven, Jenkins, Docker, Kubernetes)", score: 3, comments: "Experience with cloud services but no mention of CI/CD pipelines or Kubernetes." },
    ],
    resumeAssessment: {
      grammar: { score: 7, comments: "Some minor errors in sentence structure and awkward phrasing." },
      sentenceStructure: { score: 6, comments: "Some sentences are redundant and could be made more concise." },
      clarity: { score: 5, comments: "Resume lacks clear structure in experience section; inconsistent use of bullet points." },
    },
    workExperience: [
      { industry: "Software Development", company: "ABC Corp", years: 3, country: "USA" },
      { industry: "Cloud Services", company: "XYZ Ltd.", years: 2, country: "Canada" },
    ],
    education: [
      { degree: "BSc Computer Science", institution: "University of ABC", year: 2020 },
      { certification: "AWS Practitioner", institution: "AWS", year: 2021 },
    ],
    technicalSkills: [
      { technology: "Java", proficiency: 5, lastUsed: "2024" },
      { technology: "Python", proficiency: 6, lastUsed: "2024" },
      { technology: "AngularJS", proficiency: 4, lastUsed: "2023" },
      { technology: "AWS", proficiency: 6, lastUsed: "2024" },
    ],
    overallScore: 3.5,
    recommendation: "The candidate has a solid foundation in Java and cloud technologies but lacks hands-on experience with core job requirements such as Spring Boot, Microservices, React/Angular 8+, API development, and DevOps. Resume needs improvement in clarity, structure, and detail."
  };

  const handlePrint = () => {
    window.print();
  };

// Handle Email functionality
const handleEmailReports = async (report) => {
  const emailData = {
    to: 'recipient@example.com',
    subject: 'Selected Report',
    reports: [report], 
  };

  try {
    const response = await fetch('http://127.0.0.1:8000/api/sendemail/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(emailData),
    });

    if (!response.ok) throw new Error('Failed to send email');
    toast.success('Email sent successfully!');
  } catch (error) {
    toast.error('Failed to send email.');
    console.error('Email error:', error);
  }
};

// Handle Delete functionality
const handleDeleteReports = async (reportId) => {
  try {
    const response = await fetch(`http://127.0.0.1:8000/api/reports/${reportId}/`, {
      method: 'DELETE',
    });

    if (!response.ok) throw new Error('Failed to delete report');
    toast.success('Report deleted successfully!');
    setSelectedReports((prevReports) => prevReports.filter((report) => report.id !== reportId));
  } catch (error) {
    toast.error('Failed to delete report.');
    console.error('Delete error:', error);
  }
};



return (
  <div className="candidate-summary-container">
    <h1 className="candidate-summary-title">Candidate Summary</h1>
    <h2 className="candidate-summary-role">Name - Full Stack Developer</h2>
    
    <section className="candidate-summary-section">
      <h2 className="summary-section-title">Overall Score & Recommendation</h2>
      <p><strong>Final Score:</strong> {summaryData.overallScore}/10</p>
      <p><strong>Recommendation:</strong> {summaryData.recommendation}</p>
    </section>

    <section className="candidate-summary-section">
      <h2 className="summary-section-title">Job Requirements Scoring</h2>
      <table className="candidate-summary-table">
        <thead>
          <tr>
            <th>Requirement</th>
            <th>Score (1-10)</th>
            <th>Comments</th>
          </tr>
        </thead>
        <tbody>
          {summaryData.jobRequirements.map((item, index) => (
            <tr key={index}>
              <td>{item.requirement}</td>
              <td>{item.score}</td>
              <td>{item.comments}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </section>

    <section className="candidate-summary-section">
      <h2 className="summary-section-title">Work Experience</h2>
      <table className="candidate-summary-table">
        <thead>
          <tr>
            <th>Industry</th>
            <th>Company</th>
            <th>Years</th>
            <th>Country</th>
          </tr>
        </thead>
        <tbody>
          {summaryData.workExperience.map((item, index) => (
            <tr key={index}>
              <td>{item.industry}</td>
              <td>{item.company}</td>
              <td>{item.years}</td>
              <td>{item.country}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </section>

    <section className="candidate-summary-section">
      <h2 className="summary-section-title">Education & Certifications</h2>
      <table className="candidate-summary-table">
        <thead>
          <tr>
            <th>Degree/Certification</th>
            <th>Institution</th>
            <th>Year</th>
          </tr>
        </thead>
        <tbody>
          {summaryData.education.map((item, index) => (
            <tr key={index}>
              <td>{item.degree || item.certification}</td>
              <td>{item.institution}</td>
              <td>{item.year}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </section>

    <section className="candidate-summary-section">
      <h2 className="summary-section-title">Technical Skills</h2>
      <table className="candidate-summary-table">
        <thead>
          <tr>
            <th>Technology</th>
            <th>Proficiency (1-10)</th>
            <th>Last Used</th>
          </tr>
        </thead>
        <tbody>
          {summaryData.technicalSkills.map((item, index) => (
            <tr key={index}>
              <td>{item.technology}</td>
              <td>{item.proficiency}</td>
              <td>{item.lastUsed}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </section>

    {/* Action Buttons */}
    <div className="candidate-action-buttons">
      <button className="candidate-btn email-btn" onClick={() => handleEmailReports("Emailing")}>📧 Email</button>
      <button className="candidate-btn download-btn" onClick={() => handleDownloadReports("Downloading")}>📥 Download</button>
      <button className="candidate-btn delete-btn" onClick={handleDeleteReports}>🗑️ Delete</button>
      <button className="candidate-btn print-btn" onClick={() => handlePrint("Printing")}>🖨️ Print</button>
    </div>
  </div>
  );
};

export default Summary;
