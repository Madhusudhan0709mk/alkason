from typing import Dict, Any
from infrastructure.logging_service import LoggingService
from .data_provider_strategy import DataProviderStrategy, AlphaVantageStrategy, YahooFinanceStrategy, BrokerAPIStrategy

class DataFetcher:
    def __init__(self, config: Dict[str, Any], logging_service: LoggingService):
        self.config = config
        self.logging_service = logging_service
        self.data_provider: DataProviderStrategy = None

    async def initialize(self):
        provider_config = self.config['data_provider']
        provider_type = provider_config['type']
        if provider_type == 'alpha_vantage':
            self.data_provider = AlphaVantageStrategy(provider_config['api_key'])
        elif provider_type == 'yahoo_finance':
            self.data_provider = YahooFinanceStrategy()
        elif provider_type == 'broker_api':
            broker_api = self.config['broker_api']
            self.data_provider = BrokerAPIStrategy(broker_api)
        else:
            raise ValueError(f"Unsupported data provider: {provider_type}")
        await self.logging_service.log_info(f"DataFetcher initialized with {provider_type} provider")

    async def fetch_data(self, symbol: str) -> Dict[str, Any]:
        try:
            return await self.data_provider.fetch_data(symbol)
        except Exception as e:
            await self.logging_service.log_error(f"Error fetching data for {symbol}: {str(e)}")
            raise

    async def close(self):
        if hasattr(self.data_provider, 'close'):
            await self.data_provider.close()
        await self.logging_service.log_info("DataFetcher closed")