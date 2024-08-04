import React, { useState } from 'react';
import axios from 'axios';

const RiskManagementConfig = () => {
  const [riskConfig, setRiskConfig] = useState({
    maxLeverage: '',
    riskPerTrade: ''
  });

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setRiskConfig(prevConfig => ({
      ...prevConfig,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post('/api/risk-management', riskConfig);
      // Handle success (e.g., show a message or redirect)
    } catch (error) {
      console.error('Error updating risk management configuration:', error);
    }
  };

  return (
    <div className="risk-management-config">
      <h2>Risk Management Configuration</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Max Leverage</label>
          <input 
            name="maxLeverage" 
            type="number" 
            step="0.1" 
            value={riskConfig.maxLeverage} 
            onChange={handleInputChange} 
          />
        </div>
        <div>
          <label>Risk Per Trade (%)</label>
          <input 
            name="riskPerTrade" 
            type="number" 
            step="0.1" 
            value={riskConfig.riskPerTrade} 
            onChange={handleInputChange} 
          />
        </div>
        <button type="submit" class="btn btn-primary">Update Risk Management Configuration</button>
      </form>
    </div>
  );
};

export default RiskManagementConfig;
