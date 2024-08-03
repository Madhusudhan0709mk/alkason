import React, { useState, useEffect } from 'react';
import axios from 'axios';

const BrokerConfig = () => {
  const [brokers, setBrokers] = useState([]);
  const [newBroker, setNewBroker] = useState({
    name: '',
    apiKey: '',
    apiSecret: '',
    baseUrl: '',
    isActive: true,
    orderTypes: [],
    maxOrderSize: 0,
    commissionRate: 0,
  });

  // Fetch brokers from the server
  const fetchBrokers = async () => {
    try {
      const response = await axios.get('/api/brokers');
      setBrokers(response.data);
    } catch (error) {
      console.error('Error fetching brokers:', error);
    }
  };

  // Effect to fetch brokers on component mount
  useEffect(() => {
    fetchBrokers();
  }, []);

  // Handle form input changes
  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setNewBroker((prev) => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value,
    }));
  };

  // Handle order type checkbox changes
  const handleOrderTypeChange = (e) => {
    const { value, checked } = e.target;
    setNewBroker((prev) => ({
      ...prev,
      orderTypes: checked
        ? [...prev.orderTypes, value]
        : prev.orderTypes.filter((type) => type !== value),
    }));
  };

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post('/api/brokers', newBroker);
      fetchBrokers();
      setNewBroker({
        name: '',
        apiKey: '',
        apiSecret: '',
        baseUrl: '',
        isActive: true,
        orderTypes: [],
        maxOrderSize: 0,
        commissionRate: 0,
      });
    } catch (error) {
      console.error('Error adding broker:', error);
    }
  };

  // Handle broker updates
  const handleUpdate = async (broker) => {
    try {
      await axios.put(`/api/brokers/${broker.name}`, broker);
      fetchBrokers();
    } catch (error) {
      console.error('Error updating broker:', error);
    }
  };

  return (
    <div className="broker-config">
      <h2>Broker Configurations</h2>
      <form onSubmit={handleSubmit}>
        <input
          name="name"
          value={newBroker.name}
          onChange={handleInputChange}
          placeholder="Name"
          required
        />
        <input
          name="apiKey"
          value={newBroker.apiKey}
          onChange={handleInputChange}
          placeholder="API Key"
          required
        />
        <input
          name="apiSecret"
          value={newBroker.apiSecret}
          onChange={handleInputChange}
          placeholder="API Secret"
          required
        />
        <input
          name="baseUrl"
          value={newBroker.baseUrl}
          onChange={handleInputChange}
          placeholder="Base URL"
        />
        <input
          name="maxOrderSize"
          type="number"
          value={newBroker.maxOrderSize}
          onChange={handleInputChange}
          placeholder="Max Order Size"
        />
        <input
          name="commissionRate"
          type="number"
          step="0.001"
          value={newBroker.commissionRate}
          onChange={handleInputChange}
          placeholder="Commission Rate"
        />
        <div>
          <label>Order Types:</label>
          {['MARKET', 'LIMIT', 'STOP', 'STOP_LIMIT'].map((type) => (
            <label key={type}>
              <input
                type="checkbox"
                value={type}
                checked={newBroker.orderTypes.includes(type)}
                onChange={handleOrderTypeChange}
              />
              {type}
            </label>
          ))}
        </div>
        <label>
          <input
            name="isActive"
            type="checkbox"
            checked={newBroker.isActive}
            onChange={handleInputChange}
          />
          Active
        </label>
        <button type="submit">Add Broker</button>
      </form>
      <ul>
        {brokers.map((broker) => (
          <li key={broker.name}>
            {broker.name} - Active: {broker.isActive ? 'Yes' : 'No'}, Max Order
            Size: {broker.maxOrderSize}, Commission Rate: {broker.commissionRate}, Order
            Types: {broker.orderTypes.join(', ')}
            <button
              onClick={() =>
                handleUpdate({ ...broker, isActive: !broker.isActive })
              }
            >
              {broker.isActive ? 'Deactivate' : 'Activate'}
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default BrokerConfig;
