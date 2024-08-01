from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict
from config.config_manager import ConfigManager
from models.config_models import (StockConfigUpdate, DataProviderConfigUpdate, 
                                  BrokerConfigUpdate, AIModelConfigUpdate, 
                                  TradingStrategyUpdate, RiskManagementConfigUpdate, 
                                  SystemSettingsUpdate, DecisionEngineConfigUpdate)

router = APIRouter()

def get_config_manager():
    return ConfigManager("sqlite:///trading_system.db")

@router.get("/stocks")
async def get_stocks(config_manager: ConfigManager = Depends(get_config_manager)):
    return await config_manager.get_stock_configs()

@router.post("/stocks")
async def update_stock(stock: StockConfigUpdate, config_manager: ConfigManager = Depends(get_config_manager)):
    await config_manager.update_stock_config(stock.symbol, stock.dict())
    return {"message": "Stock configuration updated successfully"}

@router.get("/data-providers")
async def get_data_providers(config_manager: ConfigManager = Depends(get_config_manager)):
    return await config_manager.get_data_provider_configs()

@router.post("/data-providers")
async def update_data_provider(provider: DataProviderConfigUpdate, config_manager: ConfigManager = Depends(get_config_manager)):
    await config_manager.update_data_provider_config(provider.name, provider.dict())
    return {"message": "Data provider configuration updated successfully"}

@router.get("/brokers")
async def get_brokers(config_manager: ConfigManager = Depends(get_config_manager)):
    return await config_manager.get_broker_configs()

@router.post("/brokers")
async def update_broker(broker: BrokerConfigUpdate, config_manager: ConfigManager = Depends(get_config_manager)):
    await config_manager.update_broker_config(broker.name, broker.dict())
    return {"message": "Broker configuration updated successfully"}

@router.get("/ai-models")
async def get_ai_models(config_manager: ConfigManager = Depends(get_config_manager)):
    return await config_manager.get_ai_model_configs()

@router.post("/ai-models")
async def update_ai_model(model: AIModelConfigUpdate, config_manager: ConfigManager = Depends(get_config_manager)):
    await config_manager.update_ai_model_config(model.name, model.dict())
    return {"message": "AI model configuration updated successfully"}

@router.get("/trading-strategies")
async def get_trading_strategies(config_manager: ConfigManager = Depends(get_config_manager)):
    return await config_manager.get_trading_strategies()

@router.post("/trading-strategies")
async def update_trading_strategy(strategy: TradingStrategyUpdate, config_manager: ConfigManager = Depends(get_config_manager)):
    await config_manager.update_trading_strategy(strategy.name, strategy.dict())
    return {"message": "Trading strategy updated successfully"}

@router.get("/risk-management")
async def get_risk_management_config(config_manager: ConfigManager = Depends(get_config_manager)):
    return await config_manager.get_risk_management_config()

@router.put("/risk-management")
async def update_risk_management_config(config: RiskManagementConfigUpdate, config_manager: ConfigManager = Depends(get_config_manager)):
    await config_manager.update_risk_management_config(config.dict())
    return {"message": "Risk management configuration updated successfully"}

@router.get("/system-settings")
async def get_system_settings(config_manager: ConfigManager = Depends(get_config_manager)):
    return await config_manager.get_system_settings()

@router.put("/system-settings")
async def update_system_settings(settings: SystemSettingsUpdate, config_manager: ConfigManager = Depends(get_config_manager)):
    await config_manager.update_system_settings(settings.dict())
    return {"message": "System settings updated successfully"}

@router.get("/decision-engine-config")
async def get_decision_engine_config(config_manager: ConfigManager = Depends(get_config_manager)):
    try:
        return await config_manager.get_decision_engine_config()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/decision-engine-config")
async def update_decision_engine_config(config: DecisionEngineConfigUpdate, config_manager: ConfigManager = Depends(get_config_manager)):
    try:
        await config_manager.update_decision_engine_config(config.dict())
        return {"message": "Decision engine configuration updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))