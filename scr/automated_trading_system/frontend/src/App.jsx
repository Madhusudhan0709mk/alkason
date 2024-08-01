import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import Navbar from './components/Navbar';
import Dashboard from './components/Dashboard';
import Login from './components/Login';
import StockConfig from './components/StockConfig';
import DataProviderConfig from './components/DataProviderConfig';
import BrokerConfig from './components/BrokerConfig';
import AIModelConfig from './components/AIModelConfig';
import TradingStrategyConfig from './components/TradingStrategyConfig';
import RiskManagementConfig from './components/RiskManagementConfig';
import SystemSettings from './components/SystemSettings';
import PerformanceMonitoring from './components/PerformanceMonitoring';
import DecisionEngineConfig from './components/DecisionEngineConfig';

function App() {
  return (
    <Router>
      <div className="App">
        <Navbar />
        <Switch>
          <Route exact path="/" component={Dashboard} />
          <Route path="/login" component={Login} />
          <Route path="/stocks" component={StockConfig} />
          <Route path="/data-providers" component={DataProviderConfig} />
          <Route path="/brokers" component={BrokerConfig} />
          <Route path="/ai-models" component={AIModelConfig} />
          <Route path="/trading-strategies" component={TradingStrategyConfig} />
          <Route path="/risk-management" component={RiskManagementConfig} />
          <Route path="/system-settings" component={SystemSettings} />
          <Route path="/performance" component={PerformanceMonitoring} />
          <Route path="/decision-engine" component={DecisionEngineConfig} />
        </Switch>
      </div>
    </Router>
  );
}

export default App;