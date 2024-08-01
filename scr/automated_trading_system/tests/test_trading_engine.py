import pytest
from unittest.mock import AsyncMock, patch
from business_logic.trading_engine import TradingEngine

@pytest.fixture
def mock_logging_service():
    return AsyncMock()

@pytest.fixture
def mock_stock_data_manager():
    return AsyncMock()

@pytest.fixture
def mock_error_handler():
    return AsyncMock()

@pytest.fixture
def trading_engine(mock_logging_service, mock_stock_data_manager, mock_error_handler):
    config = {'trading_interval': 1}
    return TradingEngine(config, mock_logging_service, mock_stock_data_manager, mock_error_handler)

@pytest.mark.asyncio
async def test_initialize(trading_engine):
    await trading_engine.initialize()
    trading_engine.logging_service.log_info.assert_called_once_with("Initializing TradingEngine")

@pytest.mark.asyncio
async def test_trading_cycle(trading_engine):
    trading_engine.stock_data_manager.get_active_stocks.return_value = ['AAPL', 'GOOGL']
    trading_engine.stock_data_manager.get_stock_data.side_effect = [{'price': 150.0}, {'price': 2800.0}]
    
    await trading_engine.trading_cycle()
    
    assert trading_engine.stock_data_manager.get_stock_data.call_count == 2

@pytest.mark.asyncio
async def test_run(trading_engine):
    with patch.object(trading_engine, 'trading_cycle', AsyncMock()) as mock_trading_cycle:
        mock_trading_cycle.side_effect = [None, Exception("Test error"), asyncio.CancelledError()]
        
        with pytest.raises(asyncio.CancelledError):
            await trading_engine.run()
        
        assert mock_trading_cycle.call_count == 3
        trading_engine.error_handler.handle_error.assert_called_once()
