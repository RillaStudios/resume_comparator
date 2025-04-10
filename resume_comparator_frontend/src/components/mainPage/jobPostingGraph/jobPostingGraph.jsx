import React, { useEffect, useState } from 'react';
import { Line } from 'react-chartjs-2';
import axios from 'axios';
import './jobPostingGraph.css';


// Import Chart.js components
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';

// Register necessary Chart.js components
ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

const JobPostingGraph = () => {
    const [reportData, setReportData] = useState([]);

    useEffect(() => {
        // Fetch report data from Django backend
        axios.get("http://127.0.0.1:8000/api/reports/")  
            .then(response => {
                setReportData(response.data);  
            })
            .catch(error => {
                console.error('Error fetching report data:', error);
            });
    }, []);

    // Chart data structure
    const chartData = {
        labels: reportData.map(data => `ID: ${data.id}`), 
        datasets: [
            {
                label: 'Job Postings',  
                data: reportData.map(data => data.score),  
                borderColor: 'rgba(75,192,192,1)',  
                tension: 0.1,  
            },
        ],
    };

    // Chart options with axis configuration
    const chartOptions = {
        scales: {
            x: {
                type: 'category',  
            },
            y: {
                type: 'linear',  
            },
        },
    };

    return (
        <div className="jobPosting-graph-container">
            <div className="jobPosting-container-body">  
            <div className="chart">
                <h2>Job Posting Report</h2>
                <Line data={chartData} options={chartOptions} />
            </div>
        </div>
        </div>
    );
};

export default JobPostingGraph;