# File: analysis/post_trade_analysis.py

from typing import Dict, Any
import numpy as np

class PostTradeAnalysis:
    def __init__(self, config: Dict[str, Any]):
        self.config = config

    async def analyze(self, trade_data: Dict[str, Any], outcome: str) -> Dict[str, Any]:
        entry_price = trade_data['entry_price']
        exit_price = trade_data['exit_price']
        volume = trade_data['volume']
        
        pnl = (exit_price - entry_price) * volume
        pnl_percentage = (exit_price - entry_price) / entry_price * 100

        hold_time = trade_data['exit_time'] - trade_data['entry_time']
        
        max_favorable_excursion = max(trade_data['high_prices']) - entry_price if trade_data['action'] == 'BUY' else entry_price - min(trade_data['low_prices'])
        max_adverse_excursion = entry_price - min(trade_data['low_prices']) if trade_data['action'] == 'BUY' else max(trade_data['high_prices']) - entry_price

        return {
            'pnl': pnl,
            'pnl_percentage': pnl_percentage,
            'hold_time': hold_time,
            'max_favorable_excursion': max_favorable_excursion,
            'max_adverse_excursion': max_adverse_excursion,
            'outcome': outcome,
            'trade_efficiency': (pnl / max_favorable_excursion) if max_favorable_excursion != 0 else 0
        }