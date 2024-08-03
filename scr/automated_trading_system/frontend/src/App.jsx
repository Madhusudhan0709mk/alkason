import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';

import Navbar from './components/Navbar';
import Dashboard from './components/dashboard';
import StockConfig from './components/StockConfig'; 
import BrokerConfig from './components/BrokerConfig';
import AIModelConfig from './components/AIModelConfig';
import TradingStrategyConfig from './components/TradingStrategyConfig';
import RiskManagementConfig from './components/RiskManagementConfig';
import SystemSettings from './components/SystemSettings';
import PerformanceMonitoring from './components/PerformanceMonitoring';
import DecisionEngineConfig from './components/DecisionEngineConfig';

const App = () => {
  return (
    <BrowserRouter>
      <Navbar />
      <Routes>
        <Route path="/" element={<Dashboard />} />
        {/* <Route path="/login" element={<Login />} /> */}
        <Route path="/stocks" element={<StockConfig />} />
        <Route path="/brokers" element={<BrokerConfig />} /> 
        <Route path="/ai-models" element={<AIModelConfig />} />
        <Route path="/trading-strategies" element={<TradingStrategyConfig />} />
        <Route path="/risk-management" element={<RiskManagementConfig />} />
        <Route path="/system-settings" element={<SystemSettings />} />
        <Route path="/performance" element={<PerformanceMonitoring />} />
        <Route path="/decision-engine" element={<DecisionEngineConfig />} />
      </Routes>
    </BrowserRouter>
  );
};

export default App;
