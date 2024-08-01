fetchBrokers();
      setNewBroker({ 
        name: '', 
        apiKey: '', 
        apiSecret: '', 
        baseUrl: '', 
        isActive: true,
        orderTypes: [],
        maxOrderSize: 0,
        commissionRate: 0
      });
    } catch (error) {
      console.error('Error adding broker:', error);
    }
  };

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
        <input name="name" value={newBroker.name} onChange={handleInputChange} placeholder="Name" required />
        <input name="apiKey" value={newBroker.apiKey} onChange={handleInputChange} placeholder="API Key" required />
        <input name="apiSecret" value={newBroker.apiSecret} onChange={handleInputChange} placeholder="API Secret" required />
        <input name="baseUrl" value={newBroker.baseUrl} onChange={handleInputChange} placeholder="Base URL" />
        <input name="maxOrderSize" type="number" value={newBroker.maxOrderSize} onChange={handleInputChange} placeholder="Max Order Size" />
        <input name="commissionRate" type="number" step="0.001" value={newBroker.commissionRate} onChange={handleInputChange} placeholder="Commission Rate" />
        <div>
          <label>Order Types:</label>
          {['MARKET', 'LIMIT', 'STOP', 'STOP_LIMIT'].map(type => (
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
          <input name="isActive" type="checkbox" checked={newBroker.isActive} onChange={handleInputChange} />
          Active
        </label>
        <button type="submit">Add Broker</button>
      </form>
      <ul>
        {brokers.map((broker) => (
          <li key={broker.name}>
            {broker.name} - Active: {broker.isActive ? 'Yes' : 'No'}, 
            Max Order Size: {broker.maxOrderSize},
            Commission Rate: {broker.commissionRate},
            Order Types: {broker.orderTypes.join(', ')}
            <button onClick={() => handleUpdate({...broker, isActive: !broker.isActive})}>
              {broker.isActive ? 'Deactivate' : 'Activate'}
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default BrokerConfig;
