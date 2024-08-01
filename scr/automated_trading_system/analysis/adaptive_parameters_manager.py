# File: analysis/adaptive_parameters_manager.py

from typing import Dict, Any
import numpy as np
from scipy.stats import linregress

class AdaptiveParametersManager:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.default_parameters = {
            'rsi_period': 14,
            'macd_fast': 12,
            'macd_slow': 26,
            'macd_signal': 9,
            'bollinger_period': 20,
            'bollinger_std': 2
        }
        self.current_parameters = self.default_parameters.copy()

    async def adjust_parameters(self, market_data: Dict[str, Any], performance_data: Dict[str, Any]) -> Dict[str, Any]:
        volatility = self._calculate_volatility(market_data['close'])
        trend_strength = self._calculate_trend_strength(market_data['close'])
        recent_performance = performance_data.get('recent_return', 0)

        self.current_parameters['rsi_period'] = self._adjust_rsi_period(volatility)
        self.current_parameters['macd_fast'], self.current_parameters['macd_slow'] = self._adjust_macd_parameters(trend_strength)
        self.current_parameters['bollinger_std'] = self._adjust_bollinger_std(volatility, recent_performance)

        return self.current_parameters

    def _calculate_volatility(self, prices: List[float]) -> float:
        returns = np.diff(prices) / prices[:-1]
        return np.std(returns)

    def _calculate_trend_strength(self, prices: List[float]) -> float:
        x = np.arange(len(prices))
        slope, _, r_value, _, _ = linregress(x, prices)
        return abs(slope) * r_value**2

    def _adjust_rsi_period(self, volatility: float) -> int:
        base_period = self.default_parameters['rsi_period']
        if volatility > 0.02:  # High volatility
            return max(5, base_period - 4)
        elif volatility < 0.005:  # Low volatility
            return min(30, base_period + 4)
        return base_period

    def _adjust_macd_parameters(self, trend_strength: float) -> Tuple[int, int]:
        base_fast = self.default_parameters['macd_fast']
        base_slow = self.default_parameters['macd_slow']
        if trend_strength > 0.7:  # Strong trend
            return base_fast - 2, base_slow - 4
        elif trend_strength < 0.3:  # Weak trend
            return base_fast + 2, base_slow + 4
        return base_fast, base_slow

    def _adjust_bollinger_std(self, volatility: float, recent_performance: float) -> float:
        base_std = self.default_parameters['bollinger_std']
        if volatility > 0.02 and recent_performance > 0:
            return base_std + 0.5
        elif volatility < 0.005 and recent_performance < 0:
            return max(1.5, base_std - 0.5)
        return base_std