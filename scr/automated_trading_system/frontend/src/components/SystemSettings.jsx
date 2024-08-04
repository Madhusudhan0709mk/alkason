import React, { useState, useEffect } from 'react';
import axios from 'axios';

const SystemSettings = () => {
  const [settings, setSettings] = useState({
    tradingInterval: 0,
    backtestingStartDate: '',
    backtestingEndDate: '',
    paperTrading: false,
    logLevel: 'INFO',
    maxConcurrentTrades: 0,
    dataUpdateFrequency: 0
  });

  useEffect(() => {
    fetchSettings();
  }, []);

  const fetchSettings = async () => {
    try {
      const response = await axios.get('/api/system-settings');
      setSettings(response.data);
    } catch (error) {
      console.error('Error fetching system settings:', error);
    }
  };

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setSettings(prevSettings => ({
      ...prevSettings,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.put('/api/system-settings', settings);
      alert('System settings updated successfully');
    } catch (error) {
      console.error('Error updating system settings:', error);
      alert('Error updating system settings');
    }
  };

  return (
    <div className="system-settings">
      <h2>System Settings</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Trading Interval (seconds)</label>
          <input 
            name="tradingInterval" 
            type="number" 
            value={settings.tradingInterval} 
            onChange={handleInputChange} 
          />
        </div>
        <div>
          <label>Backtesting Start Date</label>
          <input 
            name="backtestingStartDate" 
            type="date" 
            value={settings.backtestingStartDate} 
            onChange={handleInputChange} 
          />
        </div>
        <div>
          <label>Backtesting End Date</label>
          <input 
            name="backtestingEndDate" 
            type="date" 
            value={settings.backtestingEndDate} 
            onChange={handleInputChange} 
          />
        </div>
        <div>
          <label>
            <input 
              name="paperTrading" 
              type="checkbox" 
              checked={settings.paperTrading} 
              onChange={handleInputChange} 
            />
            Paper Trading
          </label>
        </div>
        <div>
          <label>Log Level</label>
          <select name="logLevel" value={settings.logLevel} onChange={handleInputChange}>
            <option value="DEBUG">DEBUG</option>
            <option value="INFO">INFO</option>
            <option value="WARNING">WARNING</option>
            <option value="ERROR">ERROR</option>
            <option value="CRITICAL">CRITICAL</option>
          </select>
        </div>
        <div>
          <label>Max Concurrent Trades</label>
          <input 
            name="maxConcurrentTrades" 
            type="number" 
            value={settings.maxConcurrentTrades} 
            onChange={handleInputChange} 
          />
        </div>
        <div>
          <label>Data Update Frequency (seconds)</label>
          <input 
            name="dataUpdateFrequency" 
            type="number" 
            value={settings.dataUpdateFrequency} 
            onChange={handleInputChange} 
          />
        </div>
        <button type="submit" class="btn btn-primary">Update System Settings</button>
      </form>
    </div>
  );
};

export default SystemSettings;
