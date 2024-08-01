import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Line } from 'react-chartjs-2';

function PerformanceMonitoring() {
  const [performanceData, setPerformanceData] = useState({
    equity: [],
    returns: [],
    drawdown: [],
    trades: []
  });

  useEffect(() => {
    fetchPerformanceData();
  }, []);

  const fetchPerformanceData = async () => {
    try {
      const response = await axios.get('/api/performance');
      setPerformanceData(response.data);
    } catch (error) {
      console.error('Error fetching performance data:', error);
    }
  };

  const equityChartData = {
    labels: performanceData.equity.map(d => d.date),
    datasets: [
      {
        label: 'Equity',
        data: performanceData.equity.map(d => d.value),
        fill: false,
        borderColor: 'rgb(75, 192, 192)',
        tension: 0.1
      }
    ]
  };

  const returnsChartData = {
    labels: performanceData.returns.map(d => d.date),
    datasets: [
      {
        label: 'Returns',
        data: performanceData.returns.map(d => d.value),
        fill: false,
        borderColor: 'rgb(255, 99, 132)',
        tension: 0.1
      }
    ]
  };

  const drawdownChartData = {
    labels: performanceData.drawdown.map(d => d.date),
    datasets: [
      {
        label: 'Drawdown',
        data: performanceData.drawdown.map(d => d.value),
        fill: true,
        backgroundColor: 'rgba(255, 99, 132, 0.2)',
        borderColor: 'rgb(255, 99, 132)',
        tension: 0.1
      }
    ]
  };

  return (
    <div className="performance-monitoring">
      <h2>Performance Monitoring</h2>
      <div className="chart">
        <h3>Equity Curve</h3>
        <Line data={equityChartData} />
      </div>
      <div className="chart">
        <h3>Returns</h3>
        <Line data={returnsChartData} />
      </div>
      <div className="chart">
        <h3>Drawdown</h3>
        <Line data={drawdownChartData} />
      </div>
      <div className="trade-history">
        <h3>Recent Trades</h3>
        <table>
          <thead>
            <tr>
              <th>Date</th>
              <th>Symbol</th>
              <th>Action</th>
              <th>Price</th>
              <th>Quantity</th>
              <th>Profit/Loss</th>
            </tr>
          </thead>
          <tbody>
            {performanceData.trades.map((trade, index) => (
              <tr key={index}>
                <td>{trade.date}</td>
                <td>{trade.symbol}</td>
                <td>{trade.action}</td>
                <td>{trade.price}</td>
                <td>{trade.quantity}</td>
                <td>{trade.pnl}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default PerformanceMonitoring;
