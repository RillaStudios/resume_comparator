import React, { useEffect, useState } from 'react';
import { Pie } from 'react-chartjs-2';
import axios from 'axios';
import './jobPostingGraph.css';

// Import Chart.js components
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, ArcElement, Title, Tooltip, Legend } from 'chart.js';

// Register necessary Chart.js components
ChartJS.register(CategoryScale, LinearScale, PointElement, ArcElement, Title, Tooltip, Legend);

const JobPostingGraph = () => {
    const [reportData, setReportData] = useState([]);

    useEffect(() => {
        // Fetch report data from Django backend
        axios.get("http://127.0.0.1:8000/api/job-postings/")  
            .then(response => {
                setReportData(response.data);  
            })
            .catch(error => {
                console.error('Error fetching report data:', error);
            });
    }, []);

    // If data is empty, show a fallback
    if (reportData.length === 0) {
        return (
            <div className="jobPosting-graph-container">
                <div className="jobPosting-container-body">
                    <h2>No Job Posting Data Available</h2>
                </div>
            </div>
        );
    }

    // Chart data structure (Pie chart example)
    const chartData = {
        labels: reportData.map(data => `ID: ${data.id}`), 
        datasets: [
            {
                label: 'Job Postings',
                data: reportData.map(data => data.title.length), 
                backgroundColor: ['rgba(75,192,192,0.2)', 'rgba(153,102,255,0.2)', 'rgba(255,159,64,0.2)'],
                borderColor: ['rgba(75,192,192,1)', 'rgba(153,102,255,1)', 'rgba(255,159,64,1)'],
                borderWidth: 1
            },
        ],
    };

    // Chart options
    const chartOptions = {
        responsive: true,
        maintainAspectRatio: false, 
        plugins: {
            legend: {
                position: 'top',
            },
            tooltip: {
                enabled: true,
            },
        },
    };

    return (
        <div className="jobPosting-graph-container">
            <div className="jobPosting-container-body">  
                <div className="chart">
                    <h2>Job Posting Report</h2>
                    <Pie data={chartData} options={chartOptions} />
                </div>
            </div>
        </div>
    );
};

export default JobPostingGraph;