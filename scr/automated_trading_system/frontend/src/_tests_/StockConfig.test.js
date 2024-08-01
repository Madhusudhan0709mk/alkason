import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import axios from 'axios';
import StockConfig from '../components/StockConfig';

jest.mock('axios');

describe('StockConfig Component', () => {
  beforeEach(() => {
    axios.get.mockResolvedValue({ data: [] });
    axios.post.mockResolvedValue({ data: { message: 'Stock configuration updated successfully' } });
  });

  it('renders without crashing', async () => {
    render(<StockConfig />);
    expect(screen.getByText('Stock Configurations')).toBeInTheDocument();
  });

  it('fetches stock configurations on mount', async () => {
    render(<StockConfig />);
    await waitFor(() => expect(axios.get).toHaveBeenCalledWith('/api/stocks'));
  });

  it('adds a new stock configuration', async () => {
    render(<StockConfig />);
    
    fireEvent.change(screen.getByPlaceholder('Symbol'), { target: { value: 'AAPL' } });
    fireEvent.change(screen.getByPlaceholder('Max Position Size'), { target: { value: '100' } });
    fireEvent.change(screen.getByPlaceholder('Risk Factor'), { target: { value: '0.02' } });
    fireEvent.click(screen.getByText('Add Stock'));

    await waitFor(() => expect(axios.post).toHaveBeenCalledWith('/api/stocks', expect.objectContaining({
      symbol: 'AAPL',
      maxPositionSize: 100,
      riskFactor: 0.02,
      isActive: true
    })));
  });

  it('updates existing stock configuration', async () => {
    axios.get.mockResolvedValue({ data: [{ symbol: 'AAPL', isActive: true, maxPositionSize: 100, riskFactor: 0.02 }] });
    render(<StockConfig />);

    await waitFor(() => expect(screen.getByText('AAPL')).toBeInTheDocument());

    fireEvent.click(screen.getByText('Deactivate'));

    await waitFor(() => expect(axios.post).toHaveBeenCalledWith('/api/stocks', expect.objectContaining({
      symbol: 'AAPL',
      isActive: false
    })));
  });

  it('displays error message on API failure', async () => {
    axios.get.mockRejectedValue(new Error('API Error'));
    render(<StockConfig />);

    await waitFor(() => expect(screen.getByText('Error fetching stock configurations')).toBeInTheDocument());
  });
});