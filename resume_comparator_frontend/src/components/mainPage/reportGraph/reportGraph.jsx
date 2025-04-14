import React, { useEffect, useState } from 'react';
import { Bar } from 'react-chartjs-2'; // Import Bar chart from react-chartjs-2
import axios from 'axios';
import './reportGraph.css';

// Import Chart.js components
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js';

// Register necessary Chart.js components
ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

const ReportGraph = () => {
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

    // If data is empty, show a fallback
    if (reportData.length === 0) {
        return (
            <div className="jobPosting-graph-container">
                <div className="jobPosting-container-body">
                    <h2>No Score Data Available</h2>
                </div>
            </div>
        );
    }

    // Chart data structure for Bar Chart
    const chartData = {
        labels: reportData.map(data => `ID: ${data.id}`), 
        datasets: [
            {
                label: 'Report Scores', 
                data: reportData.map(data => data.score),  
                backgroundColor: 'rgba(75, 192, 192, 0.5)', 
                borderColor: 'rgba(75, 192, 192, 1)', 
                borderWidth: 1,
            },
        ],
    };

    // Chart options
    const chartOptions = {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            x: {
                type: 'category',
                ticks: {
                    autoSkip: true,
                    maxRotation: 45,
                    minRotation: 0,
                },
                title: {
                    display: true,
                    text: 'Report ID',
                },
            },
            y: {
                type: 'linear',
                beginAtZero: true,
                title: {
                    display: true,
                    text: 'Scores',
                },
            },
        },
        plugins: {
            legend: {
                display: true,
                position: 'top',
            },
            tooltip: {
                enabled: true,
            },
        },
    };

    return (
        <div className="report-graph-container">
            <div className="report-container-body">  
                <div className="chart">
                    <h2>Scores Report</h2>
                    <Bar data={chartData} options={chartOptions} />
                </div>
            </div>
        </div>
    );
};

export default ReportGraph;