import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
from web.web_server import WebServer

@pytest.fixture
def mock_logging_service():
    return AsyncMock()

@pytest.fixture
def mock_trading_engine():
    return AsyncMock()

@pytest.fixture
def mock_stock_data_manager():
    return AsyncMock()

@pytest.fixture
def web_server(mock_logging_service, mock_trading_engine, mock_stock_data_manager):
    config = {'allowed_origins': ['http://localhost:3000']}
    return WebServer(config, mock_logging_service, mock_trading_engine, mock_stock_data_manager)

@pytest.fixture
def client(web_server):
    web_server.initialize = AsyncMock()
    return TestClient(web_server.app)

def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Trading system is running"}

@pytest.mark.asyncio
async def test_get_stock_data(web_server, client):
    web_server.stock_data_manager.get_stock_data.return_value = {'price': 150.0}
    
    response = client.get("/stocks/AAPL")
    assert response.status_code == 200
    assert response.json() == {'price': 150.0}

@pytest.mark.asyncio
async def test_get_active_stocks(web_server, client):
    web_server.stock_data_manager.get_active_stocks.return_value = ['AAPL', 'GOOGL']
    
    response = client.get("/stocks")
    assert response.status_code == 200
    assert response.json() == ['AAPL', 'GOOGL']

@pytest.mark.asyncio
async def test_periodic_cache_refresh(web_server):
    with patch('asyncio.sleep', AsyncMock()) as mock_sleep:
        mock_sleep.side_effect = [None, asyncio.CancelledError()]
        
        with pytest.raises(asyncio.CancelledError):
            await web_server.periodic_cache_refresh()
        
        web_server.stock_data_manager.refresh_cache.assert_called_once()
        web_server.logging_service.log_info.assert_called_with("Frontend cache refreshed successfully")
