from pydantic import BaseModel, constr, conint, confloat

class StockConfigUpdate(BaseModel):
    symbol: constr(min_length=1, max_length=10)
    is_active: bool
    max_position_size: conint(gt=0)
    risk_factor: confloat(gt=0, lt=1)
    trading_hours_start: constr(regex=r'^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$')
    trading_hours_end: constr(regex=r'^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$')
    minimum_volume: conint(ge=0)

class DataProviderConfigUpdate(BaseModel):
    name: constr(min_length=1, max_length=50)
    api_key: constr(min_length=1)
    base_url: constr(min_length=1)
    is_active: bool
    data_type: constr(min_length=1)
    update_interval: conint(gt=0)
    max_requests_per_minute: conint(gt=0)

class BrokerConfigUpdate(BaseModel):
    name: constr(min_length=1, max_length=50)
    api_key: constr(min_length=1)
    api_secret: constr(min_length=1)
    base_url: constr(min_length=1)
    is_active: bool
    order_types: list
    max_order_size: conint(gt=0)
    commission_rate: confloat(ge=0, lt=1)

class AIModelConfigUpdate(BaseModel):
    name: constr(min_length=1, max_length=50)
    provider: constr(min_length=1)
    api_key: constr(min_length=1)
    model_type: constr(min_length=1)
    is_active: bool
    parameters: dict

class TradingStrategyUpdate(BaseModel):
    name: constr(min_length=1, max_length=50)
    type: constr(min_length=1)
    parameters: dict
    is_active: bool

class RiskManagementConfigUpdate(BaseModel):
    max_drawdown: confloat(gt=0, lt=1)
    max_position_size: confloat(gt=0, lt=1)
    stop_loss_percentage: confloat(gt=0, lt=1)
    take_profit_percentage: confloat(gt=0)
    max_leverage: confloat(ge=1)
    risk_per_trade: confloat(gt=0, lt=1)

class SystemSettingsUpdate(BaseModel):
    trading_interval: conint(gt=0)
    backtesting_start_date: str
    backtesting_end_date: str
    paper_trading: bool
    log_level: constr(regex='^(DEBUG|INFO|WARNING|ERROR|CRITICAL)$')
    max_concurrent_trades: conint(ge=0)
    data_update_frequency: conint(gt=0)