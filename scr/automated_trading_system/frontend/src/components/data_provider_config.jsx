import React, { useState, useEffect } from 'react';
import axios from 'axios';

const DataProviderConfig = () => {
  const [providers, setProviders] = useState([]);
  const [newProvider, setNewProvider] = useState({ 
    name: '', 
    apiKey: '', 
    baseUrl: '', 
    isActive: true,
    dataType: 'market',
    updateInterval: 60,
    maxRequestsPerMinute: 60
  });

  useEffect(() => {
    fetchProviders();
  }, []);

  const fetchProviders = async () => {
    try {
      const response = await axios.get('/api/data-providers');
      setProviders(response.data);
    } catch (error) {
      console.error('Error fetching data providers:', error);
    }
  };

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setNewProvider(prevProvider => ({
      ...prevProvider,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post('/api/data-providers', newProvider);
      fetchProviders();
      setNewProvider({ 
        name: '', 
        apiKey: '', 
        baseUrl: '', 
        isActive: true,
        dataType: 'market',
        updateInterval: 60,
        maxRequestsPerMinute: 60
      });
    } catch (error) {
      console.error('Error adding data provider:', error);
    }
  };

  const handleUpdate = async (provider) => {
    try {
      await axios.put(`/api/data-providers/${provider.name}`, provider);
      fetchProviders();
    } catch (error) {
      console.error('Error updating data provider:', error);
    }
  };

  return (
    <div className="data-provider-config">
      <h2>Data Provider Configurations</h2>
      <form onSubmit={handleSubmit}>
        <input name="name" value={newProvider.name} onChange={handleInputChange} placeholder="Name" required />
        <input name="apiKey" value={newProvider.apiKey} onChange={handleInputChange} placeholder="API Key" required />
        <input name="baseUrl" value={newProvider.baseUrl} onChange={handleInputChange} placeholder="Base URL" />
        <select name="dataType" value={newProvider.dataType} onChange={handleInputChange}>
          <option value="market">Market Data</option>
          <option value="fundamental">Fundamental Data</option>
          <option value="news">News Data</option>
        </select>
        <input name="updateInterval" type="number" value={newProvider.updateInterval} onChange={handleInputChange} placeholder="Update Interval (seconds)" />
        <input name="maxRequestsPerMinute" type="number" value={newProvider.maxRequestsPerMinute} onChange={handleInputChange} placeholder="Max Requests Per Minute" />
        <label>
          <input name="isActive" type="checkbox" checked={newProvider.isActive} onChange={handleInputChange} />
          Active
        </label>
        <button type="submit">Add Provider</button>
      </form>
      <ul>
        {providers.map((provider) => (
          <li key={provider.name}>
            {provider.name} - Active: {provider.isActive ? 'Yes' : 'No'}, 
            Data Type: {provider.dataType},
            Update Interval: {provider.updateInterval}s,
            Max Requests/Min: {provider.maxRequestsPerMinute}
            <button onClick={() => handleUpdate({...provider, isActive: !provider.isActive})}>
              {provider.isActive ? 'Deactivate' : 'Activate'}
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default DataProviderConfig;
