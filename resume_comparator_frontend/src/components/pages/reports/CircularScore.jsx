import React, { useEffect, useState } from "react";

const CircularScore = ({ score }) => {
  const radius = 36;
  const stroke = 6;
  const normalizedRadius = radius - stroke / 2;
  const circumference = 2 * Math.PI * normalizedRadius;

  const [progress, setProgress] = useState(0);
  const isPass = score >= 70;

  useEffect(() => {
    let current = 0;
    const duration = 1000;
    const stepTime = 10;
    const steps = duration / stepTime;
    const increment = score / steps;

    const interval = setInterval(() => {
      current += increment;
      if (current >= score) {
        current = score;
        clearInterval(interval);
      }
      setProgress(current);
    }, stepTime);

    return () => clearInterval(interval);
  }, [score]);

  const strokeDashoffset =
    circumference - (progress / 100) * circumference;

  const strokeColor = isPass ? "#4CAF50" : "#F44336";
  const bgColor = "#e0e0e0";

  return (
    <svg width="100" height="100" className="circular-score">
      <defs>
        <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
          <feDropShadow dx="0" dy="2" stdDeviation="2" floodColor="#ccc" />
        </filter>
      </defs>
      <circle
        r={normalizedRadius}
        cx="50"
        cy="50"
        stroke={bgColor}
        strokeWidth={stroke}
        fill="none"
      />
      <circle
        r={normalizedRadius}
        cx="50"
        cy="50"
        stroke={strokeColor}
        strokeWidth={stroke}
        fill="none"
        strokeDasharray={circumference}
        strokeDashoffset={strokeDashoffset}
        strokeLinecap="round"
        style={{
          transition: "stroke-dashoffset 0.2s linear",
          transform: "rotate(90deg)",
          transformOrigin: "center",
          filter: "url(#shadow)",
        }}
      />
      <text
        x="50"
        y="54"
        textAnchor="middle"
        fontSize="20"
        fontWeight="600"
        fill={strokeColor}
      >
        {Math.round(progress)}%
      </text>
    </svg>
  );
};

export default CircularScore;
