import React, { useState, useEffect } from 'react';
import axios from 'axios';

function TradingStrategyConfig() {
  const [strategies, setStrategies] = useState([]);
  const [newStrategy, setNewStrategy] = useState({ 
    name: '', 
    type: '',
    parameters: {},
    isActive: true
  });

  useEffect(() => {
    fetchStrategies();
  }, []);

  const fetchStrategies = async () => {
    try {
      const response = await axios.get('/api/trading-strategies');
      setStrategies(response.data);
    } catch (error) {
      console.error('Error fetching trading strategies:', error);
    }
  };

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setNewStrategy(prevStrategy => ({
      ...prevStrategy,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handleParameterChange = (e) => {
    const { name, value } = e.target;
    setNewStrategy(prevStrategy => ({
      ...prevStrategy,
      parameters: {
        ...prevStrategy.parameters,
        [name]: value
      }
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post('/api/trading-strategies', newStrategy);
      fetchStrategies();
      setNewStrategy({ 
        name: '', 
        type: '',
        parameters: {},
        isActive: true
      });
    } catch (error) {
      console.error('Error adding trading strategy:', error);
    }
  };

  const handleUpdate = async (strategy) => {
    try {
      await axios.put(`/api/trading-strategies/${strategy.name}`, strategy);
      fetchStrategies();
    } catch (error) {
      console.error('Error updating trading strategy:', error);
    }
  };

  return (
    <div className="trading-strategy-config">
      <h2>Trading Strategy Configurations</h2>
      <form onSubmit={handleSubmit}>
        <input name="name" value={newStrategy.name} onChange={handleInputChange} placeholder="Strategy Name" required />
        <select name="type" value={newStrategy.type} onChange={handleInputChange}>
          <option value="">Select Strategy Type</option>
          <option value="momentum">Momentum</option>
          <option value="mean_reversion">Mean Reversion</option>
          <option value="breakout">Breakout</option>
          <option value="ai_driven">AI-Driven</option>
        </select>
        {newStrategy.type === 'momentum' && (
          <>
            <input name="lookback_period" type="number" onChange={handleParameterChange} placeholder="Lookback Period" />
            <input name="threshold" type="number" step="0.01" onChange={handleParameterChange} placeholder="Momentum Threshold" />
          </>
        )}
        {newStrategy.type === 'mean_reversion' && (
          <>
            <input name="ma_period" type="number" onChange={handleParameterChange} placeholder="Moving Average Period" />
            <input name="std_dev" type="number" step="0.1" onChange={handleParameterChange} placeholder="Standard Deviation" />
          </>
        )}
        {newStrategy.type === 'breakout' && (
          <>
            <input name="breakout_period" type="number" onChange={handleParameterChange} placeholder="Breakout Period" />
            <input name="channel_width" type="number" step="0.01" onChange={handleParameterChange} placeholder="Channel Width" />
          </>
        )}
        {newStrategy.type === 'ai_driven' && (
          <select name="ai_model" onChange={handleParameterChange}>
            <option value="">Select AI Model</option>
            {/* Populate this with available AI models */}
          </select>
        )}
        <label>
          <input name="isActive" type="checkbox" checked={newStrategy.isActive} onChange={handleInputChange} />
          Active
        </label>
        <button type="submit">Add Strategy</button>
      </form>
      <ul>
        {strategies.map((strategy) => (
          <li key={strategy.name}>
            {strategy.name} - Type: {strategy.type}, 
            Active: {strategy.isActive ? 'Yes' : 'No'}
            <button onClick={() => handleUpdate({...strategy, isActive: !strategy.isActive})}>
              {strategy.isActive ? 'Deactivate' : 'Activate'}
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default TradingStrategyConfig;
