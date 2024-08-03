import React from 'react';
import { Link } from 'react-router-dom';

const Navbar = () => (
  <nav className="navbar navbar-expand-lg navbar-light bg-dark"  data-bs-theme="dark">
    <a className="navbar-brand" href="/">Dashboard</a>
    <button className="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
      <span className="navbar-toggler-icon"></span>
    </button>
    <div className="collapse navbar-collapse" id="navbarNav">
      <ul className="navbar-nav">
        <li className="nav-item">
          <Link className="nav-link" to="/stocks">Stocks</Link>
        </li>
        <li className="nav-item">
          <Link className="nav-link" to="/data-providers">Data Providers</Link>
        </li>
        <li className="nav-item">
          <Link className="nav-link" to="/brokers">Brokers</Link>
        </li>
        <li className="nav-item">
          <Link className="nav-link" to="/ai-models">AI Models</Link>
        </li>
        <li className="nav-item">
          <Link className="nav-link" to="/trading-strategies">Trading Strategies</Link>
        </li>
        <li className="nav-item">
          <Link className="nav-link" to="/risk-management">Risk Management</Link>
        </li>
        <li className="nav-item">
          <Link className="nav-link" to="/system-settings">System Settings</Link>
        </li>
        <li className="nav-item">
          <Link className="nav-link" to="/performance">Performance</Link>
        </li>
        <li className="nav-item">
          <Link className="nav-link" to="/decision-engine">Decision Engine</Link>
        </li>
      </ul>
    </div>
  </nav>
);

export default Navbar;
