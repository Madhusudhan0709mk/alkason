from typing import Dict, Any, List
from .pattern_matching import PatternMatcher
from .trade_decision_adjuster import TradeDecisionAdjuster
from .risk_management import RiskManagement
from analysis.main_analysis import MainAnalysis
from ai_analysis.main_ai_analysis import MainAIAnalysis
from infrastructure.logging_service import LoggingService

class DecisionEngine:
    def __init__(self, config: Dict[str, Any], 
                 pattern_matcher: PatternMatcher, 
                 trade_decision_adjuster: TradeDecisionAdjuster, 
                 risk_management: RiskManagement,
                 main_analysis: MainAnalysis,
                 main_ai_analysis: MainAIAnalysis,
                 logging_service: LoggingService):
        self.config = config
        self.pattern_matcher = pattern_matcher
        self.trade_decision_adjuster = trade_decision_adjuster
        self.risk_management = risk_management
        self.main_analysis = main_analysis
        self.main_ai_analysis = main_ai_analysis
        self.logging_service = logging_service
        self.decision_thresholds = self.config.get('decision_thresholds', {
            'confidence_threshold': 0.6,
            'volume_threshold': 1000
        })

    async def initialize(self):
        try:
            await self.main_analysis.initialize()
            await self.main_ai_analysis.initialize()
            await self.logging_service.log_info("DecisionEngine initialized successfully")
        except Exception as e:
            await self.logging_service.log_error(f"Error initializing DecisionEngine: {str(e)}")
            raise

    async def make_decision(self, combined_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            market_data = combined_data['market_data']
            news_data = combined_data['news_data']
            
            analysis_results = combined_data['analysis_results']
            ai_analysis_result = combined_data['ai_analysis_results']
            strategy_signal = combined_data['strategy_signal']
            
            advanced_results = analysis_results['advanced']
            market_regime = advanced_results['market_regime']
            anomalies = advanced_results['anomalies']
            pattern_prediction = advanced_results['prediction']

            initial_decision = self._generate_initial_decision(analysis_results, ai_analysis_result, strategy_signal)
            
            regime_adjusted_decision = self._adjust_for_market_regime(initial_decision, market_regime)
            anomaly_adjusted_decision = self._adjust_for_anomalies(regime_adjusted_decision, anomalies)
            pattern_adjusted_decision = self._adjust_for_pattern_prediction(anomaly_adjusted_decision, pattern_prediction)
            
            similar_patterns = await self.pattern_matcher.find_similar_patterns(market_data)
            final_decision = await self.trade_decision_adjuster.adjust_decision(pattern_adjusted_decision, similar_patterns)
            
            await self.logging_service.log_info(f"Decision made: {final_decision}")
            return final_decision
        except Exception as e:
            await self.logging_service.log_error(f"Error in make_decision: {str(e)}")
            raise

    def _generate_initial_decision(self, analysis_result: Dict[str, Any], ai_analysis_result: Dict[str, Any], strategy_signal: Dict[str, Any]) -> Dict[str, Any]:
        technical_indicators = analysis_result['technical']
        sentiment_analysis = analysis_result['sentiment']
        ai_recommendation = ai_analysis_result['aggregated_recommendation']
        
        decision = {
            'action': strategy_signal['action'],
            'confidence': strategy_signal['confidence'],
            'price': analysis_result['market_data']['close'][-1],
            'volume': self.decision_thresholds['volume_threshold'] if strategy_signal['action'] != 'HOLD' else 0,
            'target_price': strategy_signal['suggested_exit'],
            'stop_loss': strategy_signal['stop_loss'],
            'take_profit': strategy_signal['take_profit'],
            'reasoning': f"Strategy: {strategy_signal['reason']}; AI: {ai_recommendation['reasoning']}; Technical: {technical_indicators['summary']}; Sentiment: {sentiment_analysis['summary']}"
        }
        
        return decision

    def _adjust_for_market_regime(self, decision: Dict[str, Any], market_regime: str) -> Dict[str, Any]:
        if market_regime == "trending":
            decision['confidence'] *= 1.2  # Increase confidence in trending markets
        elif market_regime == "mean-reverting":
            decision['confidence'] *= 0.8  # Decrease confidence in mean-reverting markets
        elif market_regime == "volatile":
            decision['confidence'] *= 0.6  # Significantly decrease confidence in volatile markets
            decision['volume'] *= 0.5  # Reduce position size in volatile markets
        
        return decision

    def _adjust_for_anomalies(self, decision: Dict[str, Any], anomalies: List[int]) -> Dict[str, Any]:
        if anomalies:
            decision['confidence'] *= 0.8  # Decrease confidence if anomalies are detected
            decision['volume'] *= 0.7  # Reduce position size if anomalies are detected
        return decision

    def _adjust_for_pattern_prediction(self, decision: Dict[str, Any], pattern_prediction: Dict[str, Any]) -> Dict[str, Any]:
        if pattern_prediction['predicted_movement'] == decision['action'].lower():
            decision['confidence'] *= (1 + pattern_prediction['confidence'])
        else:
            decision['confidence'] *= (1 - pattern_prediction['confidence'])
        
        decision['confidence'] = min(1.0, decision['confidence'])  # Ensure confidence doesn't exceed 1.0
        return decision

    async def update_with_post_trade_analysis(self, post_trade_results: Dict[str, Any]):
        try:
            # Update decision thresholds based on post-trade analysis results
            if post_trade_results['outcome'] == 'success':
                self.decision_thresholds['confidence_threshold'] *= 0.99  # Slightly decrease threshold for more trades
                self.decision_thresholds['volume_threshold'] *= 1.01  # Slightly increase volume for successful trades
            else:
                self.decision_thresholds['confidence_threshold'] *= 1.01  # Slightly increase threshold for fewer trades
                self.decision_thresholds['volume_threshold'] *= 0.99  # Slightly decrease volume for unsuccessful trades

            # Ensure thresholds stay within reasonable bounds
            self.decision_thresholds['confidence_threshold'] = max(0.5, min(0.8, self.decision_thresholds['confidence_threshold']))
            self.decision_thresholds['volume_threshold'] = max(100, min(10000, self.decision_thresholds['volume_threshold']))

            # Update pattern matching weights
            await self.pattern_matcher.update_weights(post_trade_results)

            # Update trade decision adjuster parameters
            await self.trade_decision_adjuster.update_parameters(post_trade_results)

            await self.logging_service.log_info(f"DecisionEngine updated with post-trade analysis results. New thresholds: {self.decision_thresholds}")
        except Exception as e:
            await self.logging_service.log_error(f"Error in update_with_post_trade_analysis: {str(e)}")