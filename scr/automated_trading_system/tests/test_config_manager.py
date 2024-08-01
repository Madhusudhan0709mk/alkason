import pytest
from config.config_manager import ConfigManager
import os

@pytest.fixture
def config_manager():
    return ConfigManager("sqlite:///:memory:")

@pytest.mark.asyncio
async def test_load_config(config_manager):
    # Mock environment variables
    os.environ['TRADING_TEST_KEY'] = 'test_value'
    
    await config_manager.load()
    
    assert config_manager.get('test_key') == 'test_value'
    assert isinstance(config_manager.get('stocks'), dict)
    assert isinstance(config_manager.get('data_providers'), dict)

@pytest.mark.asyncio
async def test_update_stock_config(config_manager):
    await config_manager.load()
    
    stock_config = {
        'symbol': 'AAPL',
        'is_active': True,
        'max_position_size': 100
    }
    
    await config_manager.update_stock_config('AAPL', stock_config)
    
    updated_config = config_manager.get_stock_configs()
    assert 'AAPL' in updated_config
    assert updated_config['AAPL']['is_active'] == True
    assert updated_config['AAPL']['max_position_size'] == 100

@pytest.mark.asyncio
async def test_get_system_settings(config_manager):
    await config_manager.load()
    
    settings = config_manager.get_system_settings()
    assert isinstance(settings, dict)
    assert 'trading_interval' in settings
