from sqlalchemy import Column, Integer, String, Boolean, Float, JSON, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class StockConfig(Base):
    __tablename__ = 'stock_configs'

    id = Column(Integer, primary_key=True)
    symbol = Column(String, unique=True, nullable=False)
    is_active = Column(Boolean, default=True)
    max_position_size = Column(Integer)
    risk_factor = Column(Float)
    trading_hours_start = Column(String)
    trading_hours_end = Column(String)
    minimum_volume = Column(Integer)
    additional_info = Column(JSON)

class DecisionEngineConfig(Base):
    __tablename__ = 'decision_engine_config'

    id = Column(Integer, primary_key=True)
    rsi_oversold = Column(Float, nullable=False)
    rsi_overbought = Column(Float, nullable=False)
    confidence_increase = Column(Float, nullable=False)
    confidence_decrease = Column(Float, nullable=False)
    ai_disagreement_confidence_factor = Column(Float, nullable=False)
    bullish_keywords = Column(JSON, nullable=False)
    bearish_keywords = Column(JSON, nullable=False)
    risk_per_trade = Column(Float, nullable=False)

class DataProviderConfig(Base):
    __tablename__ = 'data_provider_configs'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    api_key = Column(String)
    base_url = Column(String)
    is_active = Column(Boolean, default=True)
    data_type = Column(String)
    update_interval = Column(Integer)
    max_requests_per_minute = Column(Integer)
    additional_info = Column(JSON)

class BrokerConfig(Base):
    __tablename__ = 'broker_configs'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    api_key = Column(String)
    api_secret = Column(String)
    base_url = Column(String)
    is_active = Column(Boolean, default=True)
    order_types = Column(JSON)
    max_order_size = Column(Integer)
    commission_rate = Column(Float)
    additional_info = Column(JSON)

class AIModelConfig(Base):
    __tablename__ = 'ai_model_configs'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    provider = Column(String)
    api_key = Column(String)
    model_type = Column(String)
    is_active = Column(Boolean, default=True)
    parameters = Column(JSON)

class TradingStrategy(Base):
    __tablename__ = 'trading_strategies'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    type = Column(String)
    parameters = Column(JSON)
    is_active = Column(Boolean, default=True)

class RiskManagementConfig(Base):
    __tablename__ = 'risk_management_config'

    id = Column(Integer, primary_key=True)
    max_drawdown = Column(Float)
    max_position_size = Column(Float)
    stop_loss_percentage = Column(Float)
    take_profit_percentage = Column(Float)
    max_leverage = Column(Float)
    risk_per_trade = Column(Float)

class SystemSettings(Base):
    __tablename__ = 'system_settings'

    id = Column(Integer, primary_key=True)
    trading_interval = Column(Integer)
    backtesting_start_date = Column(DateTime)
    backtesting_end_date = Column(DateTime)
    paper_trading = Column(Boolean)
    log_level = Column(String)
    max_concurrent_trades = Column(Integer)
    data_update_frequency = Column(Integer)

class PerformanceMetrics(Base):
    __tablename__ = 'performance_metrics'

    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    equity = Column(Float)
    returns = Column(Float)
    drawdown = Column(Float)

class Trade(Base):
    __tablename__ = 'trades'

    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    symbol = Column(String)
    action = Column(String)
    price = Column(Float)
    quantity = Column(Integer)
    pnl = Column(Float)