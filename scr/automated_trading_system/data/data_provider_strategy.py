from abc import ABC, abstractmethod
from typing import Dict, Any
import aiohttp
import yfinance as yf

class DataProviderStrategy(ABC):
    @abstractmethod
    async def fetch_data(self, symbol: str) -> Dict[str, Any]:
        pass

class AlphaVantageStrategy(DataProviderStrategy):
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://www.alphavantage.co/query"

    async def fetch_data(self, symbol: str) -> Dict[str, Any]:
        params = {
            "function": "TIME_SERIES_INTRADAY",
            "symbol": symbol,
            "interval": "5min",
            "apikey": self.api_key
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(self.base_url, params=params) as response:
                data = await response.json()
                if "Time Series (5min)" in data:
                    time_series = data["Time Series (5min)"]
                    latest_data = next(iter(time_series.values()))
                    return {
                        "symbol": symbol,
                        "price": float(latest_data["4. close"]),
                        "volume": int(latest_data["5. volume"]),
                        "timestamp": next(iter(time_series)),
                        "open": float(latest_data["1. open"]),
                        "high": float(latest_data["2. high"]),
                        "low": float(latest_data["3. low"]),
                        "time_series": [float(candle["4. close"]) for candle in time_series.values()]
                    }
                else:
                    raise ValueError(f"Failed to fetch data for {symbol}")

class YahooFinanceStrategy(DataProviderStrategy):
    async def fetch_data(self, symbol: str) -> Dict[str, Any]:
        stock = yf.Ticker(symbol)
        history = stock.history(period="1d", interval="5m")
        latest_data = history.iloc[-1]
        return {
            "symbol": symbol,
            "price": latest_data["Close"],
            "volume": latest_data["Volume"],
            "timestamp": latest_data.name.isoformat(),
            "open": latest_data["Open"],
            "high": latest_data["High"],
            "low": latest_data["Low"],
            "time_series": history["Close"].tolist()
        }

class BrokerAPIStrategy(DataProviderStrategy):
    def __init__(self, broker_api):
        self.broker_api = broker_api

    async def fetch_data(self, symbol: str) -> Dict[str, Any]:
        # This implementation will depend on the specific broker API
        # Here's a placeholder implementation
        data = await self.broker_api.get_stock_data(symbol)
        return {
            "symbol": symbol,
            "price": data["last_price"],
            "volume": data["volume"],
            "timestamp": data["timestamp"],
            "open": data["open"],
            "high": data["high"],
            "low": data["low"],
            "time_series": data["price_history"]
        }