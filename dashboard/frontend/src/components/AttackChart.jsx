import React, { useState, useEffect } from 'react';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

const AttackChart = () => {
  const [chartData, setChartData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchTimelineData();
    const interval = setInterval(fetchTimelineData, 60000); // Update every minute
    return () => clearInterval(interval);
  }, []);

  const fetchTimelineData = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/attacks/timeline?hours=24');
      const data = await response.json();
      
      // Process data for chart
      const hours = [];
      const services = {};
      
      // Initialize 24 hours
      for (let i = 23; i >= 0; i--) {
        const hour = new Date();
        hour.setHours(hour.getHours() - i, 0, 0, 0);
        hours.push(hour.getHours().toString().padStart(2, '0') + ':00');
      }
      
      // Group data by service
      data.forEach(item => {
        const hour = item.hour.split(' ')[1].substring(0, 5);
        if (!services[item.service]) {
          services[item.service] = new Array(24).fill(0);
        }
        const hourIndex = hours.indexOf(hour);
        if (hourIndex !== -1) {
          services[item.service][hourIndex] = item.count;
        }
      });

      const datasets = Object.keys(services).map((service, index) => ({
        label: service.toUpperCase(),
        data: services[service],
        borderColor: [
          '#00bcd4', '#ff5722', '#4caf50', '#ff9800', '#9c27b0'
        ][index % 5],
        backgroundColor: [
          'rgba(0, 188, 212, 0.1)', 'rgba(255, 87, 34, 0.1)', 
          'rgba(76, 175, 80, 0.1)', 'rgba(255, 152, 0, 0.1)', 
          'rgba(156, 39, 176, 0.1)'
        ][index % 5],
        tension: 0.4,
        fill: true,
      }));

      setChartData({
        labels: hours,
        datasets: datasets,
      });
      
      setLoading(false);
    } catch (error) {
      console.error('Failed to fetch timeline data:', error);
      setLoading(false);
    }
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'Attack Timeline (Last 24 Hours)',
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        ticks: {
          stepSize: 1,
        },
      },
      x: {
        title: {
          display: true,
          text: 'Time (Hours)',
        },
      },
    },
    interaction: {
      mode: 'index',
      intersect: false,
    },
  };

  if (loading || !chartData) {
    return <div>Loading chart...</div>;
  }

  return (
    <div style={{ height: '300px' }}>
      <Line data={chartData} options={options} />
    </div>
  );
};

export default AttackChart;
