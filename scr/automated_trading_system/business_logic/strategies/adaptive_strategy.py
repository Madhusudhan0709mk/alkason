from typing import Dict, Any, List, Tuple
from business_logic.trading_strategy_interface import TradingStrategy

class AdaptiveStrategy(TradingStrategy):
    def __init__(self, config: Dict[str, Any]):
        self.config = config

    def generate_signal(self, data: Dict[str, Any]) -> Dict[str, Any]:
        if not self.validate_data(data):
            raise ValueError("Invalid input data")

        market_regime = data['advanced']['market_regime']
        pattern_prediction = data['advanced']['prediction']
        technical_indicators = data['technical_indicators']
        sentiment_score = data['sentiment']['overall_sentiment']

        action, confidence = self._determine_action(market_regime, pattern_prediction, technical_indicators, sentiment_score)

        return {
            'action': action,
            'confidence': confidence,
            'reason': f"Market Regime: {market_regime}, Pattern Prediction: {pattern_prediction['predicted_movement']}",
            'suggested_entry': data['market_data']['close'][-1],
            'suggested_exit': self._calculate_exit_price(action, data['market_data']['close'][-1], market_regime),
            'stop_loss': self._calculate_stop_loss(action, data['market_data']['close'][-1], market_regime),
            'take_profit': self._calculate_take_profit(action, data['market_data']['close'][-1], market_regime),
        }

    def _determine_action(self, market_regime: str, pattern_prediction: Dict[str, Any], technical_indicators: Dict[str, Any], sentiment_score: float) -> Tuple[str, float]:
        if market_regime == "trending":
            return self._trending_market_strategy(pattern_prediction, technical_indicators, sentiment_score)
        elif market_regime == "mean-reverting":
            return self._mean_reverting_market_strategy(pattern_prediction, technical_indicators, sentiment_score)
        else:  # volatile
            return self._volatile_market_strategy(pattern_prediction, technical_indicators, sentiment_score)

    def _trending_market_strategy(self, pattern_prediction: Dict[str, Any], technical_indicators: Dict[str, Any], sentiment_score: float) -> Tuple[str, float]:
        if pattern_prediction['predicted_movement'] == 'up' and technical_indicators['RSI'][-1] < 70 and sentiment_score > 0:
            return 'BUY', min(pattern_prediction['confidence'] * 1.2, 1.0)
        elif pattern_prediction['predicted_movement'] == 'down' and technical_indicators['RSI'][-1] > 30 and sentiment_score < 0:
            return 'SELL', min(pattern_prediction['confidence'] * 1.2, 1.0)
        else:
            return 'HOLD', 0.5

    def _mean_reverting_market_strategy(self, pattern_prediction: Dict[str, Any], technical_indicators: Dict[str, Any], sentiment_score: float) -> Tuple[str, float]:
        if technical_indicators['RSI'][-1] < 30 and pattern_prediction['predicted_movement'] == 'up':
            return 'BUY', min(pattern_prediction['confidence'] * 1.1, 1.0)
        elif technical_indicators['RSI'][-1] > 70 and pattern_prediction['predicted_movement'] == 'down':
            return 'SELL', min(pattern_prediction['confidence'] * 1.1, 1.0)
        else:
            return 'HOLD', 0.5

    def _volatile_market_strategy(self, pattern_prediction: Dict[str, Any], technical_indicators: Dict[str, Any], sentiment_score: float) -> Tuple[str, float]:
        # In volatile markets, we're more cautious
        if pattern_prediction['predicted_movement'] == 'up' and technical_indicators['RSI'][-1] < 60 and sentiment_score > 0.2:
            return 'BUY', pattern_prediction['confidence'] * 0.8
        elif pattern_prediction['predicted_movement'] == 'down' and technical_indicators['RSI'][-1] > 40 and sentiment_score < -0.2:
            return 'SELL', pattern_prediction['confidence'] * 0.8
        else:
            return 'HOLD', 0.7  # Higher confidence in HOLD during volatile markets
    
    def _calculate_exit_price(self, action: str, current_price: float, market_regime: str) -> float:
        if market_regime == "trending":
            return current_price * (1.05 if action == 'BUY' else 0.95)
        elif market_regime == "mean-reverting":
            return current_price * (1.03 if action == 'BUY' else 0.97)
        else:  # volatile
            return current_price * (1.07 if action == 'BUY' else 0.93)

    def _calculate_stop_loss(self, action: str, current_price: float, market_regime: str) -> float:
        if market_regime == "trending":
            return current_price * (0.97 if action == 'BUY' else 1.03)
        elif market_regime == "mean-reverting":
            return current_price * (0.98 if action == 'BUY' else 1.02)
        else:  # volatile
            return current_price * (0.95 if action == 'BUY' else 1.05)

    def _calculate_take_profit(self, action: str, current_price: float, market_regime: str) -> float:
        if market_regime == "trending":
            return current_price * (1.1 if action == 'BUY' else 0.9)
        elif market_regime == "mean-reverting":
            return current_price * (1.05 if action == 'BUY' else 0.95)
        else:  # volatile
            return current_price * (1.15 if action == 'BUY' else 0.85)

    def get_required_data(self) -> List[str]:
        return ['market_data', 'technical_indicators', 'sentiment', 'advanced']