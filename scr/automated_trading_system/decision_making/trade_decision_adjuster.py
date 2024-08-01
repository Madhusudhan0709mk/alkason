# File: decision_making/trade_decision_adjuster.py

from typing import Dict, Any, List
from infrastructure.logging_service import LoggingService

class TradeDecisionAdjuster:
    def __init__(self, config: Dict[str, Any], logging_service: LoggingService):
        self.config = config
        self.logging_service = logging_service

    async def adjust_decision(self, decision: Dict[str, Any], similar_patterns: List[Dict[str, Any]]) -> Dict[str, Any]:
        try:
            if not similar_patterns:
                return decision

            success_count = sum(1 for pattern in similar_patterns if pattern['metadata']['outcome'] == 'success')
            failure_count = len(similar_patterns) - success_count

            if success_count > failure_count:
                decision['confidence'] *= 1.2  # Increase confidence
            elif failure_count > success_count:
                decision['confidence'] *= 0.8  # Decrease confidence

            decision['confidence'] = min(decision['confidence'], 1.0)  # Cap confidence at 1.0

            if success_count > 0:
                decision['volume'] = min(
                    decision['volume'] * (1 + 0.1 * success_count),
                    self.config.get('max_trade_volume', float('inf'))
                )
            else:
                decision['volume'] = max(
                    decision['volume'] * (1 - 0.1 * failure_count),
                    self.config.get('min_trade_volume', 0)
                )

            decision['reason'] += f" (Adjusted based on {success_count} similar successful patterns and {failure_count} failures)"

            await self.logging_service.log_info(f"Decision adjusted: {decision}")
            return decision
        except Exception as e:
            await self.logging_service.log_error(f"Error in adjust_decision: {str(e)}")
            return decision