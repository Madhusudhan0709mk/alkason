# File: analysis/multi_timeframe_analysis.py

from typing import Dict, Any, List
import pandas as pd
import numpy as np
from .technical_analysis import TechnicalAnalysis

class MultiTimeframeAnalysis:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.technical_analysis = TechnicalAnalysis(config)
        self.timeframes = ['1m', '5m', '15m', '1h', '4h', '1d']

    async def analyze(self, data: Dict[str, Any]) -> Dict[str, Any]:
        results = {}
        
        for timeframe in self.timeframes:
            timeframe_data = self._resample_data(data['market_data'], timeframe)
            results[timeframe] = await self.technical_analysis.analyze({'market_data': timeframe_data})
        
        results['trend_confluence'] = self._analyze_trend_confluence(results)
        results['support_resistance'] = self._analyze_support_resistance(results)
        
        return results

    def _resample_data(self, data: Dict[str, List[float]], timeframe: str) -> Dict[str, List[float]]:
        df = pd.DataFrame(data)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df.set_index('timestamp', inplace=True)
        
        resampled = df.resample(timeframe).agg({
            'open': 'first',
            'high': 'max',
            'low': 'min',
            'close': 'last',
            'volume': 'sum'
        })
        
        return resampled.to_dict('list')

    def _analyze_trend_confluence(self, results: Dict[str, Dict[str, Any]]) -> Dict[str, str]:
        trend_signals = {}
        
        for timeframe, analysis in results.items():
            if analysis['SMA_50'][-1] > analysis['SMA_200'][-1]:
                trend_signals[timeframe] = 'bullish'
            elif analysis['SMA_50'][-1] < analysis['SMA_200'][-1]:
                trend_signals[timeframe] = 'bearish'
            else:
                trend_signals[timeframe] = 'neutral'
        
        overall_trend = max(set(trend_signals.values()), key=list(trend_signals.values()).count)
        
        return {
            'overall_trend': overall_trend,
            'trend_signals': trend_signals
        }

    def _analyze_support_resistance(self, results: Dict[str, Dict[str, Any]]) -> Dict[str, List[float]]:
        support_levels = []
        resistance_levels = []
        
        for timeframe, analysis in results.items():
            support_levels.extend(analysis['BB_Lower'][-5:])
            resistance_levels.extend(analysis['BB_Upper'][-5:])
        
        support_levels = sorted(set(support_levels))
        resistance_levels = sorted(set(resistance_levels))
        
        return {
            'support_levels': support_levels,
            'resistance_levels': resistance_levels
        }