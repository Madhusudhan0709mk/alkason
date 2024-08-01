from typing import Dict, Any, List
from infrastructure.logging_service import LoggingService

class RiskManagement:
    def __init__(self, config: Dict[str, Any], logging_service: LoggingService):
        self.config = config
        self.logging_service = logging_service

    async def apply_risk_limits(self, decision: Dict[str, Any], risk_level: str, advanced_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            max_position_size = self.config.get('max_position_size', float('inf'))
            decision['volume'] = min(decision['volume'], max_position_size)

            market_regime = advanced_data['market_regime']
            anomalies = advanced_data['anomalies']

            decision = self._adjust_for_market_regime(decision, market_regime)
            decision = self._adjust_for_anomalies(decision, anomalies)

            if decision['action'] in ['BUY', 'SELL']:
                stop_loss_pct = self._calculate_stop_loss_percentage(market_regime, risk_level)
                decision['stop_loss'] = decision['price'] * (1 - stop_loss_pct) if decision['action'] == 'BUY' else decision['price'] * (1 + stop_loss_pct)

                take_profit_pct = self._calculate_take_profit_percentage(market_regime, risk_level)
                decision['take_profit'] = decision['price'] * (1 + take_profit_pct) if decision['action'] == 'BUY' else decision['price'] * (1 - take_profit_pct)

            current_drawdown = await self.calculate_current_drawdown()
            max_drawdown = self.config.get('max_drawdown', 0.1)
            if current_drawdown > max_drawdown:
                decision['action'] = 'HOLD'
                decision['reason'] = f"Maximum drawdown exceeded: {current_drawdown:.2%}"

            await self.logging_service.log_info(f"Risk limits applied: {decision}")
            return decision
        except Exception as e:
            await self.logging_service.log_error(f"Error in apply_risk_limits: {str(e)}")
            return decision

    def _adjust_for_market_regime(self, decision: Dict[str, Any], market_regime: str) -> Dict[str, Any]:
        if market_regime == "volatile":
            decision['volume'] *= 0.7  # Reduce position size in volatile markets
        elif market_regime == "mean-reverting":
            decision['volume'] *= 0.9  # Slightly reduce position size in mean-reverting markets
        return decision

    def _adjust_for_anomalies(self, decision: Dict[str, Any], anomalies: List[int]) -> Dict[str, Any]:
        if anomalies:
            decision['volume'] *= 0.8  # Reduce position size if anomalies are detected
        return decision

    def _calculate_stop_loss_percentage(self, market_regime: str, risk_level: str) -> float:
        base_stop_loss = self.config.get('base_stop_loss_percentage', 0.02)
        if market_regime == "volatile":
            base_stop_loss *= 1.5
        elif market_regime == "mean-reverting":
            base_stop_loss *= 0.8
        
        if risk_level == "high":
            base_stop_loss *= 1.2
        elif risk_level == "low":
            base_stop_loss *= 0.8
        
        return base_stop_loss

    def _calculate_take_profit_percentage(self, market_regime: str, risk_level: str) -> float:
        base_take_profit = self.config.get('base_take_profit_percentage', 0.05)
        if market_regime == "volatile":
            base_take_profit *= 1.5
        elif market_regime == "mean-reverting":
            base_take_profit *= 0.8
        
        if risk_level == "high":
            base_take_profit *= 0.8
        elif risk_level == "low":
            base_take_profit *= 1.2
        
        return base_take_profit

    async def calculate_current_drawdown(self) -> float:
        try:
            portfolio_values = self.config.get('portfolio_history', [])
            if not portfolio_values:
                return 0.0
            
            peak = max(portfolio_values)
            current_value = portfolio_values[-1]
            drawdown = (peak - current_value) / peak
            
            await self.logging_service.log_info(f"Current drawdown calculated: {drawdown:.2%}")
            return drawdown
        except Exception as e:
            await self.logging_service.log_error(f"Error in calculate_current_drawdown: {str(e)}")
            return 0.0

    async def assess_portfolio_risk(self, advanced_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            portfolio_values = self.config.get('portfolio_history', [])
            current_positions = self.config.get('current_positions', {})
            market_regime = advanced_data['market_regime']
            
            if not portfolio_values:
                return {'risk_level': 'unknown', 'reason': 'Insufficient historical data'}
            
            volatility = self._calculate_volatility(portfolio_values)
            total_exposure = sum(abs(position['value']) for position in current_positions.values())
            
            risk_level = self._determine_risk_level(volatility, total_exposure, market_regime)
            
            assessment = {
                'risk_level': risk_level,
                'volatility': volatility,
                'total_exposure': total_exposure,
                'market_regime': market_regime
            }
            
            await self.logging_service.log_info(f"Portfolio risk assessed: {assessment}")
            return assessment
        except Exception as e:
            await self.logging_service.log_error(f"Error in assess_portfolio_risk: {str(e)}")
            return {'risk_level': 'unknown', 'reason': 'Error in risk assessment'}

    def _calculate_volatility(self, portfolio_values: List[float]) -> float:
        returns = [(portfolio_values[i] - portfolio_values[i-1]) / portfolio_values[i-1] for i in range(1, len(portfolio_values))]
        return (sum(r**2 for r in returns) / len(returns))**0.5

    def _determine_risk_level(self, volatility: float, total_exposure: float, market_regime: str) -> str:
        if market_regime == "volatile":
            volatility *= 1.2
            total_exposure *= 1.2
        elif market_regime == "mean-reverting":
            volatility *= 0.8
            total_exposure *= 0.9
        
        if volatility > 0.03 or total_exposure > 0.8:
            return 'high'
        elif volatility > 0.02 or total_exposure > 0.6:
            return 'medium'
        else:
            return 'low'