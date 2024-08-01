from typing import Dict, Any, List
from .data_fetcher import DataFetcher
from .vector_database_enhancement import VectorDatabaseEnhancement
from repositories.config_repository import ConfigRepository
from infrastructure.logging_service import LoggingService
import asyncio
import time

class StockDataManager:
    def __init__(self, config: Dict[str, Any], data_fetcher: DataFetcher, 
                 config_repository: ConfigRepository, logging_service: LoggingService,
                 vector_db_enhancement: VectorDatabaseEnhancement):
        self.config = config
        self.data_fetcher = data_fetcher
        self.config_repository = config_repository
        self.logging_service = logging_service
        self.vector_db_enhancement = vector_db_enhancement
        self.active_stocks: List[str] = []
        self.stock_data: Dict[str, Dict[str, Any]] = {}
        self.cache_ttl = config.get('cache_ttl', 60)  # Cache time-to-live in seconds

    async def initialize(self):
        try:
            stock_configs = await self.config_repository.get_stock_configs()
            self.active_stocks = [config['symbol'] for config in stock_configs if config['is_active']]
            await self.data_fetcher.initialize()
            await self.logging_service.log_info(f"StockDataManager initialized with {len(self.active_stocks)} active stocks")
        except Exception as e:
            await self.logging_service.log_error(f"Error initializing StockDataManager: {str(e)}")
            raise

    async def get_stock_data(self, symbol: str) -> Dict[str, Any]:
        try:
            current_time = time.time()
            if symbol in self.stock_data and current_time - self.stock_data[symbol].get('timestamp', 0) < self.cache_ttl:
                await self.logging_service.log_info(f"Returning cached data for {symbol}")
                return self.stock_data[symbol]['data']

            await self.update_stock_data(symbol)
            return self.stock_data[symbol]['data']
        except Exception as e:
            await self.logging_service.log_error(f"Error fetching data for {symbol}: {str(e)}")
            raise

    async def update_stock_data(self, symbol: str):
        try:
            data = await self.data_fetcher.fetch_data(symbol)
            self.stock_data[symbol] = {'data': data, 'timestamp': time.time()}
            await self.vector_db_enhancement.enhance_database(data)
            await self.logging_service.log_info(f"Updated data for {symbol}")
        except Exception as e:
            await self.logging_service.log_error(f"Error updating data for {symbol}: {str(e)}")
            raise

    def get_active_stocks(self) -> List[str]:
        return self.active_stocks

    async def add_stock(self, symbol: str):
        try:
            if symbol not in self.active_stocks:
                self.active_stocks.append(symbol)
                await self.update_stock_data(symbol)
                await self.config_repository.update_stock_config(symbol, {'is_active': True})
                await self.logging_service.log_info(f"Added stock {symbol} to active stocks")
        except Exception as e:
            await self.logging_service.log_error(f"Error adding stock {symbol}: {str(e)}")
            raise

    async def remove_stock(self, symbol: str):
        try:
            if symbol in self.active_stocks:
                self.active_stocks.remove(symbol)
                if symbol in self.stock_data:
                    del self.stock_data[symbol]
                await self.config_repository.update_stock_config(symbol, {'is_active': False})
                await self.logging_service.log_info(f"Removed stock {symbol} from active stocks")
        except Exception as e:
            await self.logging_service.log_error(f"Error removing stock {symbol}: {str(e)}")
            raise

    async def refresh_cache(self):
        try:
            await self.logging_service.log_info("Starting cache refresh")
            refresh_tasks = [self.update_stock_data(symbol) for symbol in self.active_stocks]
            await asyncio.gather(*refresh_tasks)
            await self.logging_service.log_info("Cache refresh completed")
        except Exception as e:
            await self.logging_service.log_error(f"Error refreshing cache: {str(e)}")
            raise

    async def find_similar_patterns(self, symbol: str, k: int = 5) -> List[Dict[str, Any]]:
        try:
            if symbol not in self.stock_data:
                await self.update_stock_data(symbol)
            data = self.stock_data[symbol]['data']
            return await self.vector_db_enhancement.find_similar_patterns(data, k)
        except Exception as e:
            await self.logging_service.log_error(f"Error finding similar patterns for {symbol}: {str(e)}")
            raise

    def get_cached_symbols(self) -> List[str]:
        return list(self.stock_data.keys())

    async def clear_cache(self):
        try:
            self.stock_data.clear()
            await self.logging_service.log_info("Cache cleared")
        except Exception as e:
            await self.logging_service.log_error(f"Error clearing cache: {str(e)}")
            raise

    async def get_market_overview(self) -> Dict[str, Any]:
        try:
            overview = {}
            for symbol in self.active_stocks:
                data = await self.get_stock_data(symbol)
                overview[symbol] = {
                    'last_price': data['last_price'],
                    'change_percent': data['change_percent'],
                    'volume': data['volume']
                }
            return overview
        except Exception as e:
            await self.logging_service.log_error(f"Error getting market overview: {str(e)}")
            raise

    async def get_historical_data(self, symbol: str, start_date: str, end_date: str) -> List[Dict[str, Any]]:
        try:
            historical_data = await self.data_fetcher.fetch_historical_data(symbol, start_date, end_date)
            return historical_data
        except Exception as e:
            await self.logging_service.log_error(f"Error getting historical data for {symbol}: {str(e)}")
            raise

    async def close(self):
        try:
            await self.data_fetcher.close()
            await self.logging_service.log_info("StockDataManager closed")
        except Exception as e:
            await self.logging_service.log_error(f"Error closing StockDataManager: {str(e)}")
            raise