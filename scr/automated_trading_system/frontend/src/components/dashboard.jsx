import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Dashboard = () => {
  const [systemStatus, setSystemStatus] = useState({});
  const [recentTrades, setRecentTrades] = useState([]);


  useEffect(() => {
    fetchSystemStatus();
    fetchRecentTrades();
  }, []);

  const fetchSystemStatus = async () => {
    try {
      const response = await axios.get('/api/system/status');
      setSystemStatus(response.data);
    } catch (error) {
      console.error('Error fetching system status:', error);
    }
  };

  const fetchRecentTrades = async () => {
    try {
      const response = await axios.get('/api/trades/recent');
      console.log(response.data); // Check if this is an array
      setRecentTrades(response.data);
    } catch (error) {
      console.error('Error fetching recent trades:', error);
    }
  };
  

  return (
    <div className="dashboard">
      <h1>Trading System Dashboard</h1>
      <div className="system-status">
        <h2>System Status</h2>
        <p>Active: {systemStatus.isActive ? 'Yes' : 'No'}</p>
        <p>CPU Usage: {systemStatus.cpuUsage}%</p>
        <p>Memory Usage: {systemStatus.memoryUsage}%</p>
        <p>Active Stocks: {systemStatus.activeStocksCount}</p>
      </div>
      <div className="recent-trades">
  <h2>Recent Trades</h2>
  <ul>
    {Array.isArray(recentTrades) ? (
      recentTrades.map((trade, index) => (
        <li key={index}>
          {trade.symbol} - {trade.action} - {trade.price} - {trade.timestamp}
        </li>
      ))
    ) : (
      <li>No recent trades available.</li>
    )}
  </ul>
</div>
    </div>
  );
}

export default Dashboard;
