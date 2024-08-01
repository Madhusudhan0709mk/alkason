import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Card, CardHeader, CardContent } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Alert, AlertDescription } from '@/components/ui/alert';

function DecisionEngineConfig() {
  const [config, setConfig] = useState({
    rsi_oversold: 30,
    rsi_overbought: 70,
    confidence_increase: 0.1,
    confidence_decrease: 0.1,
    ai_disagreement_confidence_factor: 0.5,
    bullish_keywords: [],
    bearish_keywords: [],
    risk_per_trade: 0.02
  });
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);

  useEffect(() => {
    fetchConfig();
  }, []);

  const fetchConfig = async () => {
    try {
      const response = await axios.get('/api/decision-engine-config');
      setConfig(response.data);
    } catch (error) {
      setError('Error fetching decision engine configuration');
      console.error('Error fetching decision engine configuration:', error);
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setConfig(prevConfig => ({
      ...prevConfig,
      [name]: name.includes('keywords') ? value.split(',').map(k => k.trim()) : parseFloat(value)
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.put('/api/decision-engine-config', config);
      setSuccess(true);
      setError(null);
    } catch (error) {
      setError('Error updating decision engine configuration');
      setSuccess(false);
      console.error('Error updating decision engine configuration:', error);
    }
  };

  return (
    <Card className="decision-engine-config">
      <CardHeader>Decision Engine Configuration</CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label htmlFor="rsi_oversold">RSI Oversold</label>
              <Input
                id="rsi_oversold"
                name="rsi_oversold"
                type="number"
                step="0.1"
                value={config.rsi_oversold}
                onChange={handleInputChange}
              />
            </div>
            <div>
              <label htmlFor="rsi_overbought">RSI Overbought</label>
              <Input
                id="rsi_overbought"
                name="rsi_overbought"
                type="number"
                step="0.1"
                value={config.rsi_overbought}
                onChange={handleInputChange}
              />
            </div>
            <div>
              <label htmlFor="confidence_increase">Confidence Increase</label>
              <Input
                id="confidence_increase"
                name="confidence_increase"
                type="number"
                step="0.01"
                value={config.confidence_increase}
                onChange={handleInputChange}
              />
            </div>
            <div>
              <label htmlFor="confidence_decrease">Confidence Decrease</label>
              <Input
                id="confidence_decrease"
                name="confidence_decrease"
                type="number"
                step="0.01"
                value={config.confidence_decrease}
                onChange={handleInputChange}
              />
            </div>
            <div>
              <label htmlFor="ai_disagreement_confidence_factor">AI Disagreement Confidence Factor</label>
              <Input
                id="ai_disagreement_confidence_factor"
                name="ai_disagreement_confidence_factor"
                type="number"
                step="0.01"
                value={config.ai_disagreement_confidence_factor}
                onChange={handleInputChange}
              />
            </div>
            <div>
              <label htmlFor="bullish_keywords">Bullish Keywords (comma-separated)</label>
              <Input
                id="bullish_keywords"
                name="bullish_keywords"
                type="text"
                value={config.bullish_keywords.join(', ')}
                onChange={handleInputChange}
              />
            </div>
            <div>
              <label htmlFor="bearish_keywords">Bearish Keywords (comma-separated)</label>
              <Input
                id="bearish_keywords"
                name="bearish_keywords"
                type="text"
                value={config.bearish_keywords.join(', ')}
                onChange={handleInputChange}
              />
            </div>
            <div>
              <label htmlFor="risk_per_trade">Risk Per Trade</label>
              <Input
                id="risk_per_trade"
                name="risk_per_trade"
                type="number"
                step="0.01"
                value={config.risk_per_trade}
                onChange={handleInputChange}
              />
            </div>
          </div>
          {error && (
            <Alert variant="destructive">
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}
          {success && (
            <Alert>
              <AlertDescription>Configuration updated successfully</AlertDescription>
            </Alert>
          )}
          <Button type="submit">Update Decision Engine Configuration</Button>
        </form>
      </CardContent>
    </Card>
  );
}

export default DecisionEngineConfig;