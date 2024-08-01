import pytest
from unittest.mock import MagicMock, AsyncMock
from data.stock_data_manager import StockDataManager

@pytest.fixture
def mock_data_fetcher():
    return AsyncMock()

@pytest.fixture
def mock_config_repository():
    return AsyncMock()

@pytest.fixture
def mock_logging_service():
    return AsyncMock()

@pytest.fixture
def stock_data_manager(mock_data_fetcher, mock_config_repository, mock_logging_service):
    config = {'cache_ttl': 60}
    return StockDataManager(config, mock_data_fetcher, mock_config_repository, mock_logging_service)

@pytest.mark.asyncio
async def test_initialize(stock_data_manager):
    mock_stock_configs = [{'symbol': 'AAPL', 'is_active': True}, {'symbol': 'GOOGL', 'is_active': False}]
    stock_data_manager.config_repository.get_stock_configs.return_value = mock_stock_configs
    
    await stock_data_manager.initialize()
    
    assert stock_data_manager.active_stocks == ['AAPL']
    stock_data_manager.data_fetcher.initialize.assert_called_once()

@pytest.mark.asyncio
async def test_get_stock_data(stock_data_manager):
    stock_data_manager.data_fetcher.fetch_data.return_value = {'price': 150.0}
    
    data = await stock_data_manager.get_stock_data('AAPL')
    
    assert data == {'price': 150.0}
    stock_data_manager.data_fetcher.fetch_data.assert_called_once_with('AAPL')

@pytest.mark.asyncio
async def test_refresh_cache(stock_data_manager):
    stock_data_manager.active_stocks = ['AAPL', 'GOOGL']
    stock_data_manager.data_fetcher.fetch_data.side_effect = [{'price': 150.0}, {'price': 2800.0}]
    
    await stock_data_manager.refresh_cache()
    
    assert stock_data_manager.data_fetcher.fetch_data.call_count == 2
    assert 'AAPL' in stock_data_manager.stock_data
    assert 'GOOGL' in stock_data_manager.stock_data
