# File: business_logic/strategies/moving_average_crossover_strategy.py

from typing import Dict, Any, List
from business_logic.trading_strategy_interface import TradingStrategy

class MovingAverageCrossoverStrategy(TradingStrategy):
    def __init__(self, short_period: int = 10, long_period: int = 50):
        self.short_period = short_period
        self.long_period = long_period

    def generate_signal(self, data: Dict[str, Any]) -> Dict[str, Any]:
        if not self.validate_data(data):
            raise ValueError("Invalid input data")

        technical_indicators = data['technical_indicators']
        current_price = data['market_data']['price']
        short_ma = technical_indicators[f'SMA_{self.short_period}'][-1]
        long_ma = technical_indicators[f'SMA_{self.long_period}'][-1]

        if short_ma > long_ma:
            action = 'BUY'
            confidence = min((short_ma - long_ma) / long_ma, 1.0)
            reason = f"Short-term MA ({short_ma:.2f}) is above long-term MA ({long_ma:.2f})"
        elif short_ma < long_ma:
            action = 'SELL'
            confidence = min((long_ma - short_ma) / long_ma, 1.0)
            reason = f"Short-term MA ({short_ma:.2f}) is below long-term MA ({long_ma:.2f})"
        else:
            action = 'HOLD'
            confidence = 0.5
            reason = "Moving averages are equal"

        return {
            'action': action,
            'confidence': confidence,
            'reason': reason,
            'suggested_entry': current_price,
            'suggested_exit': current_price * (1.05 if action == 'BUY' else 0.95),
            'stop_loss': current_price * (0.98 if action == 'BUY' else 1.02),
            'take_profit': current_price * (1.1 if action == 'BUY' else 0.9),
        }

    def get_required_data(self) -> List[str]:
        return ['market_data', 'technical_indicators']
