from typing import List, Dict, Any
from repositories.config_repository import ConfigRepository
from infrastructure.logging_service import LoggingService

class StockWatchlist:
    def __init__(self, config_repository: ConfigRepository, logging_service: LoggingService):
        self.config_repository = config_repository
        self.logging_service = logging_service
        self.watchlist: List[Dict[str, Any]] = []

    async def initialize(self):
        self.watchlist = await self.config_repository.get_stock_configs()
        await self.logging_service.log_info(f"StockWatchlist initialized with {len(self.watchlist)} stocks")

    async def add_stock(self, symbol: str, additional_info: Dict[str, Any] = None):
        if not any(stock['symbol'] == symbol for stock in self.watchlist):
            stock_info = {'symbol': symbol, 'is_active': True}
            if additional_info:
                stock_info.update(additional_info)
            self.watchlist.append(stock_info)
            await self.config_repository.add_stock_config(stock_info)
            await self.logging_service.log_info(f"Added stock {symbol} to watchlist")

    async def remove_stock(self, symbol: str):
        self.watchlist = [stock for stock in self.watchlist if stock['symbol'] != symbol]
        await self.config_repository.remove_stock_config(symbol)
        await self.logging_service.log_info(f"Removed stock {symbol} from watchlist")

    def get_watchlist(self) -> List[Dict[str, Any]]:
        return self.watchlist

    def get_active_stocks(self) -> List[str]:
        return [stock['symbol'] for stock in self.watchlist if stock['is_active']]

    async def update_stock_status(self, symbol: str, is_active: bool):
        for stock in self.watchlist:
            if stock['symbol'] == symbol:
                stock['is_active'] = is_active
                await self.config_repository.update_stock_config(stock)
                await self.logging_service.log_info(f"Updated status for stock {symbol}: active = {is_active}")
                break

    async def update_stock_info(self, symbol: str, info: Dict[str, Any]):
        for stock in self.watchlist:
            if stock['symbol'] == symbol:
                stock.update(info)
                await self.config_repository.update_stock_config(stock)
                await self.logging_service.log_info(f"Updated info for stock {symbol}")
                break

    async def get_stock_info(self, symbol: str) -> Dict[str, Any]:
        for stock in self.watchlist:
            if stock['symbol'] == symbol:
                return stock
        await self.logging_service.log_warning(f"Stock {symbol} not found in watchlist")
        return None