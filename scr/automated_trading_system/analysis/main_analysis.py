from typing import Dict, Any, List
import numpy as np
from .technical_analysis import TechnicalAnalysis
from .sentiment_analysis import SentimentAnalysis
from .intermarket_analysis import IntermarketAnalysis
from .pattern_analysis import PatternAnalysis
from .volume_analysis import VolumeAnalysis
from .trend_analysis import TrendAnalysis
from .multi_timeframe_analysis import MultiTimeframeAnalysis
from .adaptive_parameters_manager import AdaptiveParametersManager
from data.vector_database_enhancement import VectorDatabaseEnhancement
from infrastructure.logging_service import LoggingService

class MainAnalysis:
    def __init__(self, config: Dict[str, Any], logging_service: LoggingService, vector_db_enhancement: VectorDatabaseEnhancement):
        self.config = config
        self.logging_service = logging_service
        self.technical_analysis = TechnicalAnalysis(config)
        self.sentiment_analysis = SentimentAnalysis(config)
        self.intermarket_analysis = IntermarketAnalysis(config)
        self.pattern_analysis = PatternAnalysis(config)
        self.volume_analysis = VolumeAnalysis(config)
        self.trend_analysis = TrendAnalysis(config)
        self.multi_timeframe_analysis = MultiTimeframeAnalysis(config)
        self.adaptive_parameters_manager = AdaptiveParametersManager(config)
        self.vector_db_enhancement = vector_db_enhancement

    async def initialize(self):
        try:
            await self.technical_analysis.initialize()
            await self.sentiment_analysis.initialize()
            await self.intermarket_analysis.initialize()
            await self.pattern_analysis.initialize()
            await self.volume_analysis.initialize()
            await self.trend_analysis.initialize()
            await self.multi_timeframe_analysis.initialize()
            await self.adaptive_parameters_manager.initialize()
            await self.logging_service.log_info("MainAnalysis initialized successfully")
        except Exception as e:
            await self.logging_service.log_error(f"Error initializing MainAnalysis: {str(e)}")
            raise

    async def analyze(self, market_data: Dict[str, Any], news_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        try:
            adapted_parameters = await self.adaptive_parameters_manager.adjust_parameters(market_data)
            self.config.update(adapted_parameters)

            technical_results = await self.technical_analysis.analyze(market_data)
            sentiment_results = await self.sentiment_analysis.analyze(news_data)
            intermarket_results = await self.intermarket_analysis.analyze(market_data)
            pattern_results = await self.pattern_analysis.analyze(market_data)
            volume_results = await self.volume_analysis.analyze(market_data)
            trend_results = await self.trend_analysis.analyze(market_data)
            multi_timeframe_results = await self.multi_timeframe_analysis.analyze(market_data)

            advanced_results = await self.perform_advanced_analysis(market_data, technical_results, sentiment_results)

            combined_results = {
                'technical': technical_results,
                'sentiment': sentiment_results,
                'intermarket': intermarket_results,
                'patterns': pattern_results,
                'volume': volume_results,
                'trend': trend_results,
                'multi_timeframe': multi_timeframe_results,
                'advanced': advanced_results,
                'adapted_parameters': adapted_parameters
            }

            await self.vector_db_enhancement.enhance_database(combined_results)

            analysis_summary = self.get_analysis_summary(combined_results)
            combined_results['summary'] = analysis_summary

            await self.logging_service.log_info(f"Analysis completed for symbol: {market_data.get('symbol', 'Unknown')}")
            return combined_results
        except Exception as e:
            await self.logging_service.log_error(f"Error in MainAnalysis.analyze: {str(e)}")
            raise

    async def perform_advanced_analysis(self, market_data: Dict[str, Any], technical_results: Dict[str, Any], sentiment_results: Dict[str, Any]) -> Dict[str, Any]:
        try:
            market_regime = self.detect_market_regime(technical_results, sentiment_results)
            anomalies = self.detect_anomalies(market_data)
            pattern_prediction = await self.vector_db_enhancement.find_similar_patterns(market_data)

            return {
                'market_regime': market_regime,
                'anomalies': anomalies,
                'prediction': pattern_prediction
            }
        except Exception as e:
            await self.logging_service.log_error(f"Error in perform_advanced_analysis: {str(e)}")
            raise

    def detect_market_regime(self, technical_results: Dict[str, Any], sentiment_results: Dict[str, Any]) -> str:
        trend_strength = technical_results.get('trend_strength', 0.5)
        volatility = technical_results.get('volatility', 0.5)
        sentiment = sentiment_results.get('overall_sentiment', 0)

        if trend_strength > 0.7 and abs(sentiment) > 0.5:
            return "trending"
        elif volatility > 0.7:
            return "volatile"
        else:
            return "mean-reverting"

    def detect_anomalies(self, market_data: Dict[str, Any]) -> List[int]:
        returns = np.diff(market_data['close']) / market_data['close'][:-1]
        mean = np.mean(returns)
        std = np.std(returns)
        z_scores = (returns - mean) / std
        return [i for i, z in enumerate(z_scores) if abs(z) > 3]

    def get_analysis_summary(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        summary = {
            'overall_trend': self._determine_overall_trend(analysis_results),
            'risk_level': self._assess_risk_level(analysis_results),
            'confidence_score': self._calculate_confidence_score(analysis_results),
            'key_indicators': self._extract_key_indicators(analysis_results),
        }
        return summary

    def _determine_overall_trend(self, analysis_results: Dict[str, Any]) -> str:
        technical_trend = analysis_results['technical']['trend']
        sentiment = analysis_results['sentiment']['overall_sentiment']
        volume_trend = analysis_results['volume']['volume_trend']
        
        trend_score = 0
        trend_score += 1 if technical_trend == 'bullish' else -1 if technical_trend == 'bearish' else 0
        trend_score += 1 if sentiment > 0.2 else -1 if sentiment < -0.2 else 0
        trend_score += 1 if volume_trend == 'increasing' else -1 if volume_trend == 'decreasing' else 0
        
        if trend_score > 1:
            return 'bullish'
        elif trend_score < -1:
            return 'bearish'
        else:
            return 'neutral'

    def _assess_risk_level(self, analysis_results: Dict[str, Any]) -> str:
        volatility = analysis_results['technical'].get('volatility', 0)
        rsi = analysis_results['technical'].get('RSI', [50])[-1]
        sentiment_volatility = analysis_results['sentiment'].get('sentiment_volatility', 0)
        market_breadth = analysis_results['intermarket'].get('market_breadth', 0.5)
        
        risk_factors = [
            1 if volatility > 0.02 else 0.5 if volatility > 0.01 else 0,
            1 if rsi > 70 or rsi < 30 else 0.5 if rsi > 60 or rsi < 40 else 0,
            1 if sentiment_volatility > 0.5 else 0.5 if sentiment_volatility > 0.3 else 0,
            1 if market_breadth < 0.3 or market_breadth > 0.7 else 0.5 if market_breadth < 0.4 or market_breadth > 0.6 else 0
        ]
        
        avg_risk = sum(risk_factors) / len(risk_factors)
        
        if avg_risk > 0.7:
            return 'high'
        elif avg_risk > 0.3:
            return 'medium'
        else:
            return 'low'

    def _calculate_confidence_score(self, analysis_results: Dict[str, Any]) -> float:
        technical_score = analysis_results['technical'].get('trend_strength', 0.5)
        sentiment_score = abs(analysis_results['sentiment'].get('overall_sentiment', 0))
        pattern_score = analysis_results['patterns'].get('pattern_reliability', 0.5)
        volume_score = analysis_results['volume'].get('volume_confidence', 0.5)
        intermarket_score = analysis_results['intermarket'].get('correlation_strength', 0.5)
        
        weights = {
            'technical': 0.3,
            'sentiment': 0.2,
            'pattern': 0.15,
            'volume': 0.15,
            'intermarket': 0.2
        }
        
        weighted_score = (
            technical_score * weights['technical'] +
            sentiment_score * weights['sentiment'] +
            pattern_score * weights['pattern'] +
            volume_score * weights['volume'] +
            intermarket_score * weights['intermarket']
        )
        
        return max(0, min(1, weighted_score))

    def _extract_key_indicators(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        return {
            'rsi': analysis_results['technical'].get('RSI', [])[-1],
            'macd': analysis_results['technical'].get('MACD', [])[-1],
            'bollinger_bandwidth': analysis_results['technical'].get('BB_Bandwidth', [])[-1],
            'sentiment_score': analysis_results['sentiment'].get('overall_sentiment', 0),
            'volume_trend': analysis_results['volume'].get('volume_trend', ''),
            'market_regime': analysis_results['advanced'].get('market_regime', ''),
            'pattern_prediction': analysis_results['advanced'].get('prediction', {}).get('predicted_movement', '')
        }

    async def update_with_post_trade_analysis(self, post_trade_results: Dict[str, Any]):
        try:
            await self.adaptive_parameters_manager.update_parameters(post_trade_results)
            await self.vector_db_enhancement.update_pattern(post_trade_results)
            await self.logging_service.log_info("MainAnalysis updated with post-trade analysis results")
        except Exception as e:
            await self.logging_service.log_error(f"Error in update_with_post_trade_analysis: {str(e)}")