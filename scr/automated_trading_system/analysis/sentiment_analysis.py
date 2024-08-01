# File: analysis/sentiment_analysis.py

from typing import Dict, Any
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
import requests
import pandas as pd
import numpy as np

class SentimentAnalysis:
    def __init__(self, config):
        self.config = config
        self.client = self._initialize_client()

    def _initialize_client(self):
        key = self.config['sentiment_analysis']['azure_text_analytics']['key']
        endpoint = self.config['sentiment_analysis']['azure_text_analytics']['endpoint']
        return TextAnalyticsClient(endpoint, AzureKeyCredential(key))

    async def analyze(self, data: Dict[str, Any]) -> Dict[str, Any]:
        news_text = data.get('news', '')
        social_media_text = data.get('social_media', '')
        market_data = data.get('market_data', {})
        
        results = {}
        
        # Azure Text Analytics sentiment analysis
        results['news_sentiment'] = self._analyze_text_sentiment(news_text)
        results['social_media_sentiment'] = self._analyze_text_sentiment(social_media_text)
        
        # Fear and Greed Index
        results['fear_greed_index'] = self._calculate_fear_greed_index(market_data)
        
        # Market breadth indicators
        results['market_breadth'] = self._calculate_market_breadth(market_data)
        
        # Put/Call ratio
        results['put_call_ratio'] = self._calculate_put_call_ratio(market_data)
        
        # VIX (Volatility Index)
        results['vix'] = self._get_vix_data()
        
        # COT report analysis
        results['cot_analysis'] = self._analyze_cot_report(data.get('cot_data', {}))

        return results

    def _analyze_text_sentiment(self, text: str) -> Dict[str, float]:
        try:
            response = self.client.analyze_sentiment([text])[0]
            return {
                'sentiment': response.sentiment,
                'positive_score': response.confidence_scores.positive,
                'neutral_score': response.confidence_scores.neutral,
                'negative_score': response.confidence_scores.negative
            }
        except Exception as e:
            print(f"Error in sentiment analysis: {str(e)}")
            return {
                'sentiment': 'neutral',
                'positive_score': 0.33,
                'neutral_score': 0.34,
                'negative_score': 0.33
            }

    def _calculate_fear_greed_index(self, market_data: Dict[str, Any]) -> float:
        # Simplified Fear and Greed Index calculation
        # This is a placeholder and should be replaced with a more sophisticated calculation
        returns = pd.Series(market_data['close']).pct_change()
        volatility = returns.std()
        average_return = returns.mean()
        
        if volatility == 0:
            return 50  # Neutral if there's no volatility
        
        fear_greed = 50 + (average_return / volatility) * 50
        return max(0, min(100, fear_greed))

    def _calculate_market_breadth(self, market_data: Dict[str, Any]) -> Dict[str, float]:
        # Simplified market breadth calculation
        # This should be expanded with real market-wide data
        advances = sum(1 for price in market_data['close'] if price > market_data['open'][0])
        declines = len(market_data['close']) - advances
        
        return {
            'advance_decline_ratio': advances / declines if declines else float('inf'),
            'percentage_advances': advances / len(market_data['close']) * 100
        }

    def _calculate_put_call_ratio(self, market_data: Dict[str, Any]) -> float:
        # This is a placeholder and should be replaced with actual options data
        return market_data.get('put_volume', 1000) / market_data.get('call_volume', 1000)

    def _get_vix_data(self) -> float:
        # This should be replaced with an actual API call to get VIX data
        return 20.0  # Placeholder value

    def _analyze_cot_report(self, cot_data: Dict[str, Any]) -> Dict[str, Any]:
        # Simplified COT report analysis
        # This should be expanded with more sophisticated analysis
        return {
            'net_commercial_position': cot_data.get('commercial_long', 0) - cot_data.get('commercial_short', 0),
            'net_non_commercial_position': cot_data.get('non_commercial_long', 0) - cot_data.get('non_commercial_short', 0)
        }