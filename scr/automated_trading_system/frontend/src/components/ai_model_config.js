import React, { useState, useEffect } from 'react';
import axios from 'axios';

function AIModelConfig() {
  const [aiModels, setAIModels] = useState([]);
  const [newModel, setNewModel] = useState({ 
    name: '', 
    provider: '',
    apiKey: '',
    modelType: '',
    isActive: true,
    parameters: {}
  });

  useEffect(() => {
    fetchAIModels();
  }, []);

  const fetchAIModels = async () => {
    try {
      const response = await axios.get('/api/ai-models');
      setAIModels(response.data);
    } catch (error) {
      console.error('Error fetching AI models:', error);
    }
  };

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setNewModel(prevModel => ({
      ...prevModel,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handleParameterChange = (e) => {
    const { name, value } = e.target;
    setNewModel(prevModel => ({
      ...prevModel,
      parameters: {
        ...prevModel.parameters,
        [name]: value
      }
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post('/api/ai-models', newModel);
      fetchAIModels();
      setNewModel({ 
        name: '', 
        provider: '',
        apiKey: '',
        modelType: '',
        isActive: true,
        parameters: {}
      });
    } catch (error) {
      console.error('Error adding AI model:', error);
    }
  };

  const handleUpdate = async (model) => {
    try {
      await axios.put(`/api/ai-models/${model.name}`, model);
      fetchAIModels();
    } catch (error) {
      console.error('Error updating AI model:', error);
    }
  };

  return (
    <div className="ai-model-config">
      <h2>AI Model Configurations</h2>
      <form onSubmit={handleSubmit}>
        <input name="name" value={newModel.name} onChange={handleInputChange} placeholder="Model Name" required />
        <input name="provider" value={newModel.provider} onChange={handleInputChange} placeholder="Provider" required />
        <input name="apiKey" value={newModel.apiKey} onChange={handleInputChange} placeholder="API Key" required />
        <select name="modelType" value={newModel.modelType} onChange={handleInputChange}>
          <option value="">Select Model Type</option>
          <option value="sentiment">Sentiment Analysis</option>
          <option value="prediction">Price Prediction</option>
          <option value="classification">Market Classification</option>
        </select>
        {newModel.modelType === 'sentiment' && (
          <input name="threshold" type="number" step="0.1" onChange={handleParameterChange} placeholder="Sentiment Threshold" />
        )}
        {newModel.modelType === 'prediction' && (
          <input name="horizon" type="number" onChange={handleParameterChange} placeholder="Prediction Horizon (days)" />
        )}
        {newModel.modelType === 'classification' && (
          <input name="classes" onChange={handleParameterChange} placeholder="Classes (comma-separated)" />
        )}
        <label>
          <input name="isActive" type="checkbox" checked={newModel.isActive} onChange={handleInputChange} />
          Active
        </label>
        <button type="submit">Add AI Model</button>
      </form>
      <ul>
        {aiModels.map((model) => (
          <li key={model.name}>
            {model.name} - Provider: {model.provider}, 
            Type: {model.modelType},
            Active: {model.isActive ? 'Yes' : 'No'}
            <button onClick={() => handleUpdate({...model, isActive: !model.isActive})}>
              {model.isActive ? 'Deactivate' : 'Activate'}
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default AIModelConfig;
