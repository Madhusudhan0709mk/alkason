# File: ai_analysis/main_ai_analysis.py

from typing import Dict, Any, List
import numpy as np
from .data_preparation import DataPreparation
from .ai_recommendation_system import AIRecommendationSystem
from .ai_performance_tracker import AIPerformanceTracker
from infrastructure.logging_service import LoggingService

class MainAIAnalysis:
    def __init__(self, config: Dict[str, Any], data_preparation: DataPreparation,
                 recommendation_system: AIRecommendationSystem,
                 performance_tracker: AIPerformanceTracker,
                 logging_service: LoggingService):
        self.config = config
        self.data_preparation = data_preparation
        self.recommendation_system = recommendation_system
        self.performance_tracker = performance_tracker
        self.logging_service = logging_service

    async def initialize(self):
        try:
            await self.recommendation_system.initialize()
            await self.logging_service.log_info("MainAIAnalysis initialized successfully")
        except Exception as e:
            await self.logging_service.log_error(f"Error initializing MainAIAnalysis: {str(e)}")
            raise

    async def analyze(self, market_data: Dict[str, Any], news_data: List[Dict[str, Any]], analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        try:
            prepared_data = self.data_preparation.prepare_data(market_data, news_data, analysis_results)
            recommendations = await self.recommendation_system.get_recommendations(prepared_data)
            aggregated_recommendation = self.recommendation_system.aggregate_recommendations(recommendations)
            
            return {
                'recommendations': recommendations,
                'aggregated_recommendation': aggregated_recommendation
            }
        except Exception as e:
            await self.logging_service.log_error(f"Error in MainAIAnalysis.analyze: {str(e)}")
            raise

    async def track_performance(self, analysis_results: Dict[str, Any], actual_outcome: Dict[str, Any]):
        try:
            for provider, recommendation in analysis_results['recommendations'].items():
                await self.performance_tracker.track_performance(provider, recommendation, actual_outcome)
            
            await self.performance_tracker.track_performance('aggregated', analysis_results['aggregated_recommendation'], actual_outcome)
        except Exception as e:
            await self.logging_service.log_error(f"Error in track_performance: {str(e)}")

    async def generate_performance_report(self) -> Dict[str, Any]:
        try:
            return await self.performance_tracker.generate_performance_report()
        except Exception as e:
            await self.logging_service.log_error(f"Error in generate_performance_report: {str(e)}")
            raise

    async def generate_trading_insights(self, market_overview: Dict[str, Any]) -> Dict[str, Any]:
        try:
            # Implement logic to generate overall market insights
            # This involves analyzing multiple stocks, market trends, etc.
            
            # 1. Analyze market breadth
            advancing_stocks = sum(1 for stock in market_overview['stocks'] if stock['price_change'] > 0)
            declining_stocks = sum(1 for stock in market_overview['stocks'] if stock['price_change'] < 0)
            market_breadth = advancing_stocks / (advancing_stocks + declining_stocks)

            # 2. Analyze sector performance
            sector_performance = self._analyze_sector_performance(market_overview['stocks'])

            # 3. Identify market trends
            market_trend = self._identify_market_trend(market_overview['index_data'])

            # 4. Analyze volume trends
            volume_trend = self._analyze_volume_trend(market_overview['volume_data'])

            # 5. Identify top performing and bottom performing stocks
            top_performers, bottom_performers = self._identify_top_bottom_performers(market_overview['stocks'])

            # 6. Analyze overall market sentiment
            market_sentiment = self._analyze_market_sentiment(market_overview['news_sentiment'])

            # 7. Identify potential market anomalies
            anomalies = self._identify_market_anomalies(market_overview['stocks'])

            # 8. Generate overall market summary
            market_summary = self._generate_market_summary(
                market_breadth, sector_performance, market_trend, volume_trend,
                top_performers, bottom_performers, market_sentiment, anomalies
            )

            insights = {
                'market_breadth': market_breadth,
                'sector_performance': sector_performance,
                'market_trend': market_trend,
                'volume_trend': volume_trend,
                'top_performers': top_performers,
                'bottom_performers': bottom_performers,
                'market_sentiment': market_sentiment,
                'anomalies': anomalies,
                'market_summary': market_summary
            }

            await self.logging_service.log_info("Generated trading insights successfully")
            return insights

        except Exception as e:
            await self.logging_service.log_error(f"Error in generate_trading_insights: {str(e)}")
            raise

    def _analyze_sector_performance(self, stocks: List[Dict[str, Any]]) -> Dict[str, float]:
        sector_performance = {}
        for stock in stocks:
            if stock['sector'] not in sector_performance:
                sector_performance[stock['sector']] = []
            sector_performance[stock['sector']].append(stock['price_change_percent'])
        
        return {sector: np.mean(performances) for sector, performances in sector_performance.items()}

    def _identify_market_trend(self, index_data: List[float]) -> str:
        short_term_ma = np.mean(index_data[-10:])
        long_term_ma = np.mean(index_data[-30:])
        
        if short_term_ma > long_term_ma:
            return 'Bullish'
        elif short_term_ma < long_term_ma:
            return 'Bearish'
        else:
            return 'Neutral'

    def _analyze_volume_trend(self, volume_data: List[int]) -> str:
        recent_volume = np.mean(volume_data[-5:])
        historical_volume = np.mean(volume_data[:-5])
        
        if recent_volume > historical_volume * 1.2:
            return 'Increasing'
        elif recent_volume < historical_volume * 0.8:
            return 'Decreasing'
        else:
            return 'Stable'

    def _identify_top_bottom_performers(self, stocks: List[Dict[str, Any]]) -> Tuple[List[str], List[str]]:
        sorted_stocks = sorted(stocks, key=lambda x: x['price_change_percent'], reverse=True)
        top_performers = [stock['symbol'] for stock in sorted_stocks[:5]]
        bottom_performers = [stock['symbol'] for stock in sorted_stocks[-5:]]
        return top_performers, bottom_performers

    def _analyze_market_sentiment(self, news_sentiment: List[float]) -> str:
        avg_sentiment = np.mean(news_sentiment)
        if avg_sentiment > 0.2:
            return 'Positive'
        elif avg_sentiment < -0.2:
            return 'Negative'
        else:
            return 'Neutral'

    def _identify_market_anomalies(self, stocks: List[Dict[str, Any]]) -> List[str]:
        anomalies = []
        for stock in stocks:
            if abs(stock['price_change_percent']) > 10:
                anomalies.append(f"Large move in {stock['symbol']}: {stock['price_change_percent']}%")
            if stock['volume'] > stock['avg_volume'] * 3:
                anomalies.append(f"Unusual volume in {stock['symbol']}: {stock['volume']} vs avg {stock['avg_volume']}")
        return anomalies

    def _generate_market_summary(self, market_breadth: float, sector_performance: Dict[str, float],
                                 market_trend: str, volume_trend: str, top_performers: List[str],
                                 bottom_performers: List[str], market_sentiment: str, anomalies: List[str]) -> str:
        summary = f"The market is currently showing a {market_trend} trend with {volume_trend} volume. "
        summary += f"Market breadth is {'positive' if market_breadth > 0.5 else 'negative'} at {market_breadth:.2f}. "
        best_sector = max(sector_performance, key=sector_performance.get)
        worst_sector = min(sector_performance, key=sector_performance.get)
        summary += f"The best performing sector is {best_sector} at {sector_performance[best_sector]:.2f}%, "
        summary += f"while the worst is {worst_sector} at {sector_performance[worst_sector]:.2f}%. "
        summary += f"Top performers include {', '.join(top_performers)}, "
        summary += f"while {', '.join(bottom_performers)} are underperforming. "
        summary += f"Overall market sentiment based on news is {market_sentiment}. "
        if anomalies:
            summary += f"Notable market anomalies: {'; '.join(anomalies)}."
        return summary