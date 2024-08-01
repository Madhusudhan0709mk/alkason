from typing import Dict, Any, List
import asyncpg

class ConfigRepository:
    def __init__(self, db_config: Dict[str, Any]):
        self.db_config = db_config
        self.pool = None

    async def initialize(self):
        self.pool = await asyncpg.create_pool(**self.db_config)
        
    async def get_decision_engine_config(self) -> Dict[str, Any]:
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow("SELECT * FROM decision_engine_config LIMIT 1")
            return dict(row) if row else {}
        
    async def update_decision_engine_config(self, config: Dict[str, Any]):
        async with self.pool.acquire() as conn:
            await conn.execute("""
                UPDATE decision_engine_config
                SET rsi_oversold = $1, rsi_overbought = $2, confidence_increase = $3,
                    confidence_decrease = $4, ai_disagreement_confidence_factor = $5,
                    bullish_keywords = $6, bearish_keywords = $7, risk_per_trade = $8
                WHERE id = 1
            """, config['rsi_oversold'], config['rsi_overbought'], config['confidence_increase'],
                config['confidence_decrease'], config['ai_disagreement_confidence_factor'],
                config['bullish_keywords'], config['bearish_keywords'], config['risk_per_trade'])
            
    async def get_stock_configs(self) -> List[Dict[str, Any]]:
        async with self.pool.acquire() as conn:
            rows = await conn.fetch("SELECT * FROM stock_configs")
            return [dict(row) for row in rows]

    async def add_stock_config(self, stock_info: Dict[str, Any]):
        async with self.pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO stock_configs (symbol, is_active, additional_info)
                VALUES ($1, $2, $3)
            """, stock_info['symbol'], stock_info['is_active'], stock_info.get('additional_info'))

    async def remove_stock_config(self, symbol: str):
        async with self.pool.acquire() as conn:
            await conn.execute("DELETE FROM stock_configs WHERE symbol = $1", symbol)

    async def update_stock_config(self, stock_info: Dict[str, Any]):
        async with self.pool.acquire() as conn:
            await conn.execute("""
                UPDATE stock_configs
                SET is_active = $2, additional_info = $3
                WHERE symbol = $1
            """, stock_info['symbol'], stock_info['is_active'], stock_info.get('additional_info'))

    async def get_data_provider_config(self) -> Dict[str, Any]:
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow("SELECT * FROM data_provider_configs WHERE is_active = true")
            return dict(row) if row else {}

    async def get_broker_configs(self) -> List[Dict[str, Any]]:
        async with self.pool.acquire() as conn:
            rows = await conn.fetch("SELECT * FROM broker_configs WHERE is_active = true")
            return [dict(row) for row in rows]

    async def get_system_settings(self) -> Dict[str, Any]:
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow("SELECT * FROM system_settings LIMIT 1")
            return dict(row) if row else {}

    async def update_system_settings(self, settings: Dict[str, Any]):
        async with self.pool.acquire() as conn:
            await conn.execute("""
                UPDATE system_settings
                SET trading_interval = $1, backtesting_start_date = $2, backtesting_end_date = $3,
                    paper_trading = $4, log_level = $5, max_concurrent_trades = $6, data_update_frequency = $7,
                    vector_db_snapshot_frequency = $8
                WHERE id = 1
            """, settings['trading_interval'], settings['backtesting_start_date'], settings['backtesting_end_date'],
                settings['paper_trading'], settings['log_level'], settings['max_concurrent_trades'],
                settings['data_update_frequency'], settings['vector_db_snapshot_frequency'])

    async def get_vector_db_config(self) -> Dict[str, Any]:
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow("SELECT * FROM vector_db_config LIMIT 1")
            return dict(row) if row else {}

    async def update_vector_db_config(self, config: Dict[str, Any]):
        async with self.pool.acquire() as conn:
            await conn.execute("""
                UPDATE vector_db_config
                SET snapshot_frequency = $1, dimension = $2
                WHERE id = 1
            """, config['snapshot_frequency'], config['dimension'])

    async def close(self):
        if self.pool:
            await self.pool.close()