import React from 'react';
import { Link } from 'react-router-dom';

function Navbar() {
  return (
    <nav className="navbar">
      <ul>
        <li><Link to="/">Dashboard</Link></li>
        <li><Link to="/stocks">Stocks</Link></li>
        <li><Link to="/data-providers">Data Providers</Link></li>
        <li><Link to="/brokers">Brokers</Link></li>
        <li><Link to="/ai-models">AI Models</Link></li>
        <li><Link to="/trading-strategies">Trading Strategies</Link></li>
        <li><Link to="/risk-management">Risk Management</Link></li>
        <li><Link to="/system-settings">System Settings</Link></li>
        <li><Link to="/performance">Performance</Link></li>
        <li><Link to="/decision-engine">Decision Engine</Link></li>
      </ul>
    </nav>
  );
}

export default Navbar;