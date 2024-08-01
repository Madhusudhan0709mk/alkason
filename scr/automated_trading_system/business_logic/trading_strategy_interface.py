# File: business_logic/trading_strategy_interface.py

from abc import ABC, abstractmethod
from typing import Dict, Any, List

class TradingStrategy(ABC):
    @abstractmethod
    def generate_signal(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a trading signal based on the provided data.
        
        :param data: A dictionary containing market data and analysis results
        :return: A dictionary containing the trading signal details
        """
        pass

    @abstractmethod
    def get_required_data(self) -> List[str]:
        """
        Return a list of required data fields for this strategy.
        
        :return: A list of required data field names as strings
        """
        pass

    def validate_data(self, data: Dict[str, Any]) -> bool:
        """
        Validate that the input data contains all required fields.
        
        :param data: A dictionary containing all input data
        :return: True if data is valid, False otherwise
        """
        required_fields = self.get_required_data()
        return all(field in data for field in required_fields)

    @classmethod
    def get_strategy_name(cls) -> str:
        """
        Return the name of the strategy.
        
        :return: The name of the strategy as a string
        """
        return cls.__name__

class CombinedStrategy(TradingStrategy):
    def __init__(self, strategies: List[TradingStrategy], weights: List[float] = None):
        self.strategies = strategies
        if weights is None:
            self.weights = [1/len(strategies)] * len(strategies)
        else:
            assert len(weights) == len(strategies), "Number of weights must match number of strategies"
            assert abs(sum(weights) - 1.0) < 1e-6, "Weights must sum to 1"
            self.weights = weights

    def generate_signal(self, data: Dict[str, Any]) -> Dict[str, Any]:
        signals = []
        for strategy in self.strategies:
            if strategy.validate_data(data):
                signals.append(strategy.generate_signal(data))
            else:
                raise ValueError(f"Invalid data for strategy: {strategy.get_strategy_name()}")

        combined_action = self._combine_actions([s['action'] for s in signals])
        combined_confidence = sum(s['confidence'] * w for s, w in zip(signals, self.weights))
        combined_reason = "; ".join([f"{s.get_strategy_name()}: {s['reason']}" for s in signals])

        return {
            'action': combined_action,
            'confidence': combined_confidence,
            'reason': combined_reason,
            'suggested_entry': self._weighted_average([s.get('suggested_entry', data['market_data']['price']) for s in signals]),
            'suggested_exit': self._weighted_average([s.get('suggested_exit', data['market_data']['price']) for s in signals]),
            'stop_loss': min(s.get('stop_loss', data['market_data']['price']) for s in signals),
            'take_profit': max(s.get('take_profit', data['market_data']['price']) for s in signals),
        }

    def get_required_data(self) -> List[str]:
        return list(set().union(*[s.get_required_data() for s in self.strategies]))

    def _combine_actions(self, actions: List[str]) -> str:
        buy_count = actions.count('BUY')
        sell_count = actions.count('SELL')
        hold_count = actions.count('HOLD')
        
        if buy_count > sell_count and buy_count > hold_count:
            return 'BUY'
        elif sell_count > buy_count and sell_count > hold_count:
            return 'SELL'
        else:
            return 'HOLD'

    def _weighted_average(self, values: List[float]) -> float:
        return sum(v * w for v, w in zip(values, self.weights))