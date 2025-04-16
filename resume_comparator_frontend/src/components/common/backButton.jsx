import React from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowLeft } from 'lucide-react';
import './BackButton.css'; // Import the CSS file

const BackButton = () => {
  const navigate = useNavigate();

  return (
    <button onClick={() => navigate(-1)} className="back-button-container">
      <ArrowLeft className="back-button-icon" />
      <span className="back-button-text">Back</span>
    </button>
  );
};

export default BackButton;
