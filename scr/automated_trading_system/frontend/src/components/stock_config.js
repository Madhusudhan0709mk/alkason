import React, { useState, useEffect } from 'react';
import axios from 'axios';

function StockConfig() {
  const [stocks, setStocks] = useState([]);
  const [newStock, setNewStock] = useState({ 
    symbol: '', 
    isActive: true, 
    maxPositionSize: 0, 
    riskFactor: 0,
    tradingHours: { start: '09:30', end: '16:00' },
    minimumVolume: 0
  });

  useEffect(() => {
    fetchStocks();
  }, []);

  const fetchStocks = async () => {
    try {
      const response = await axios.get('/api/stocks');
      setStocks(response.data);
    } catch (error) {
      console.error('Error fetching stocks:', error);
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setNewStock(prevStock => ({
      ...prevStock,
      [name]: name === 'isActive' ? e.target.checked : value
    }));
  };

  const handleTradingHoursChange = (e) => {
    const { name, value } = e.target;
    setNewStock(prevStock => ({
      ...prevStock,
      tradingHours: {
        ...prevStock.tradingHours,
        [name]: value
      }
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post('/api/stocks', newStock);
      fetchStocks();
      setNewStock({ 
        symbol: '', 
        isActive: true, 
        maxPositionSize: 0, 
        riskFactor: 0,
        tradingHours: { start: '09:30', end: '16:00' },
        minimumVolume: 0
      });
    } catch (error) {
      console.error('Error adding stock:', error);
    }
  };

  const handleUpdate = async (stock) => {
    try {
      await axios.put(`/api/stocks/${stock.symbol}`, stock);
      fetchStocks();
    } catch (error) {
      console.error('Error updating stock:', error);
    }
  };

  return (
    <div className="stock-config">
      <h2>Stock Configurations</h2>
      <form onSubmit={handleSubmit}>
        <input name="symbol" value={newStock.symbol} onChange={handleInputChange} placeholder="Symbol" required />
        <input name="maxPositionSize" type="number" value={newStock.maxPositionSize} onChange={handleInputChange} placeholder="Max Position Size" />
        <input name="riskFactor" type="number" step="0.01" value={newStock.riskFactor} onChange={handleInputChange} placeholder="Risk Factor" />
        <input name="minimumVolume" type="number" value={newStock.minimumVolume} onChange={handleInputChange} placeholder="Minimum Volume" />
        <div>
          <label>Trading Hours:</label>
          <input name="start" type="time" value={newStock.tradingHours.start} onChange={handleTradingHoursChange} />
          <input name="end" type="time" value={newStock.tradingHours.end} onChange={handleTradingHoursChange} />
        </div>
        <label>
          <input name="isActive" type="checkbox" checked={newStock.isActive} onChange={handleInputChange} />
          Active
        </label>
        <button type="submit">Add Stock</button>
      </form>
      <ul>
        {stocks.map((stock) => (
          <li key={stock.symbol}>
            {stock.symbol} - Active: {stock.isActive ? 'Yes' : 'No'}, 
            Max Position Size: {stock.maxPositionSize}, 
            Risk Factor: {stock.riskFactor},
            Minimum Volume: {stock.minimumVolume},
            Trading Hours: {stock.tradingHours.start} - {stock.tradingHours.end}
            <button onClick={() => handleUpdate({...stock, isActive: !stock.isActive})}>
              {stock.isActive ? 'Deactivate' : 'Activate'}
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default StockConfig;
