# Automated Trading System

## Overview

This project is an automated trading system designed to analyze market data, make trading decisions, and execute trades automatically. It integrates various analysis techniques, including technical analysis, sentiment analysis, and AI-driven predictions.

## Features

- Real-time market data processing
- Technical analysis using multiple indicators
- Sentiment analysis of news and social media
- AI-driven market predictions
- Risk management and position sizing
- Multi-broker support for order execution
- Web-based configuration interface
- Performance monitoring and reporting

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/your-username/automated-trading-system.git
   ```

2. Install backend dependencies:
   ```
   cd automated-trading-system
   pip install -r requirements.txt
   ```

3. Install frontend dependencies:
   ```
   cd frontend
   npm install
   ```

## Configuration

1. Copy `.env.example` to `.env` and fill in your configuration details.
2. Update `config/settings.yaml` with your specific trading parameters.

## Usage

1. Start the backend server:
   ```
   python main.py
   ```

2. Start the frontend development server:
   ```
   cd frontend
   npm start
   ```

3. Access the web interface at `http://localhost:3000`

## Testing

Run backend tests:
```
pytest tests/
```

Run frontend tests:
```
cd frontend
npm test
```