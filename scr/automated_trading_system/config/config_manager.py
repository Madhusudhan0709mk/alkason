import yaml
import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from database.models import Base, StockConfig, DataProviderConfig, BrokerConfig, AIModelConfig, TradingStrategy, RiskManagementConfig, SystemSettings, DecisionEngineConfig
from typing import Dict, Any, List
from infrastructure.logging_service import LoggingService

class ConfigManager:
    def __init__(self, db_url: str, logging_service: LoggingService):
        self.config = {}
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)
        Base.metadata.create_all(self.engine)
        self.logging_service = logging_service

    async def load(self):
        try:
            with open('config/settings.yaml', 'r') as file:
                self.config = yaml.safe_load(file)
            
            for key, value in os.environ.items():
                if key.startswith('TRADING_'):
                    self.config[key.replace('TRADING_', '').lower()] = self._parse_env_value(value)

            azure_openai_config = self.config.get('azure_openai', {})
            self.config['azure_openai_deployment'] = azure_openai_config.get('deployment_name')
            self.config['azure_openai_model'] = azure_openai_config.get('model_name')
            self.config['azure_openai_api_base'] = azure_openai_config.get('api_base')
            self.config['azure_openai_api_version'] = azure_openai_config.get('api_version')
            self.config['azure_openai_api_key'] = azure_openai_config.get('api_key')

            await self.load_db_configs()
            await self.logging_service.log_info("Configuration loaded successfully")
        except Exception as e:
            await self.logging_service.log_error(f"Error loading configuration: {str(e)}")
            raise

    def get(self, key, default=None):
        return self.config.get(key, default)

    async def update(self, key: str, value: Any):
        try:
            self.config[key] = value
            await self.update_db_config(key, value)
            await self.logging_service.log_info(f"Configuration updated: {key}")
        except Exception as e:
            await self.logging_service.log_error(f"Error updating configuration: {str(e)}")
            raise

    def _parse_env_value(self, value: str) -> Any:
        if value.lower() == 'true':
            return True
        elif value.lower() == 'false':
            return False
        try:
            return int(value)
        except ValueError:
            try:
                return float(value)
            except ValueError:
                return value

    async def load_db_configs(self):
        with self.Session() as session:
            self.config['stocks'] = {stock.symbol: self._row2dict(stock) for stock in session.query(StockConfig).all()}
            self.config['data_providers'] = {provider.name: self._row2dict(provider) for provider in session.query(DataProviderConfig).all()}
            self.config['brokers'] = {broker.name: self._row2dict(broker) for broker in session.query(BrokerConfig).all()}
            self.config['ai_models'] = {model.name: self._row2dict(model) for model in session.query(AIModelConfig).all()}
            self.config['trading_strategies'] = {strategy.name: self._row2dict(strategy) for strategy in session.query(TradingStrategy).all()}
            self.config['risk_management'] = self._row2dict(session.query(RiskManagementConfig).first())
            self.config['system_settings'] = self._row2dict(session.query(SystemSettings).first())
            self.config['decision_engine'] = self._row2dict(session.query(DecisionEngineConfig).first())

    async def update_db_config(self, key: str, value: Any):
        with self.Session() as session:
            if key == 'stocks':
                await self._update_stocks(session, value)
            elif key == 'data_providers':
                await self._update_data_providers(session, value)
            elif key == 'brokers':
                await self._update_brokers(session, value)
            elif key == 'ai_models':
                await self._update_ai_models(session, value)
            elif key == 'trading_strategies':
                await self._update_trading_strategies(session, value)
            elif key == 'risk_management':
                await self._update_risk_management(session, value)
            elif key == 'system_settings':
                await self._update_system_settings(session, value)
            elif key == 'decision_engine':
                await self._update_decision_engine(session, value)
            session.commit()

    async def _update_stocks(self, session, stocks: Dict[str, Any]):
        for symbol, config in stocks.items():
            stock = session.query(StockConfig).filter_by(symbol=symbol).first()
            if stock:
                for key, value in config.items():
                    setattr(stock, key, value)
            else:
                session.add(StockConfig(symbol=symbol, **config))

    def _row2dict(self, row):
        return {column.name: getattr(row, column.name) for column in row.__table__.columns}

    async def get_stock_configs(self) -> List[Dict[str, Any]]:
        return list(self.config.get('stocks', {}).values())
    
    async def get_decision_engine_config(self) -> Dict[str, Any]:
        try:
            return self.config.get('decision_engine', {})
        except Exception as e:
            await self.logging_service.log_error(f"Error fetching decision engine configuration: {str(e)}")
            raise

    async def update_stock_config(self, symbol: str, config: Dict[str, Any]):
        try:
            with self.Session() as session:
                stock = session.query(StockConfig).filter_by(symbol=symbol).first()
                if stock:
                    for key, value in config.items():
                        setattr(stock, key, value)
                else:
                    stock = StockConfig(symbol=symbol, **config)
                    session.add(stock)
                session.commit()
            self.config['stocks'][symbol] = config
            await self.logging_service.log_info(f"Stock configuration updated: {symbol}")
        except Exception as e:
            await self.logging_service.log_error(f"Error updating stock configuration: {str(e)}")
            raise

    async def get_system_settings(self) -> Dict[str, Any]:
        return self.config.get('system_settings', {})

    async def update_system_settings(self, settings: Dict[str, Any]):
        try:
            with self.Session() as session:
                system_settings = session.query(SystemSettings).first()
                if system_settings:
                    for key, value in settings.items():
                        setattr(system_settings, key, value)
                else:
                    system_settings = SystemSettings(**settings)
                    session.add(system_settings)
                session.commit()
            self.config['system_settings'] = settings
            await self.logging_service.log_info("System settings updated")
        except Exception as e:
            await self.logging_service.log_error(f"Error updating system settings: {str(e)}")
            raise

    async def update_decision_engine_config(self, config: Dict[str, Any]):
        try:
            with self.Session() as session:
                decision_engine = session.query(DecisionEngineConfig).first()
                if decision_engine:
                    for key, value in config.items():
                        setattr(decision_engine, key, value)
                else:
                    decision_engine = DecisionEngineConfig(**config)
                    session.add(decision_engine)
                session.commit()
            self.config['decision_engine'] = config
            await self.logging_service.log_info("Decision engine configuration updated")
        except Exception as e:
            await self.logging_service.log_error(f"Error updating decision engine configuration: {str(e)}")
            raise

    async def _update_decision_engine(self, session, config: Dict[str, Any]):
        decision_engine = session.query(DecisionEngineConfig).first()
        if decision_engine:
            for key, value in config.items():
                setattr(decision_engine, key, value)
        else:
            decision_engine = DecisionEngineConfig(**config)
            session.add(decision_engine)