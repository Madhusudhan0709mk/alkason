# File: analysis/pattern_analysis.py

import talib
import numpy as np
from typing import Dict, Any

class PatternAnalysis:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.patterns = {
            'CDLHAMMER': talib.CDLHAMMER,
            'CDLSHOOTINGSTAR': talib.CDLSHOOTINGSTAR,
            'CDLDOJI': talib.CDLDOJI,
            'CDLENGULFING': talib.CDLENGULFING,
            'CDLMORNINGSTAR': talib.CDLMORNINGSTAR,
            'CDLEVENINGSTAR': talib.CDLEVENINGSTAR,
            'CDLHARAMI': talib.CDLHARAMI,
            'CDL3WHITESOLDIERS': talib.CDL3WHITESOLDIERS,
            'CDL3BLACKCROWS': talib.CDL3BLACKCROWS,
            'CDLPIERCING': talib.CDLPIERCING,
            'CDLDARKCLOUDCOVER': talib.CDLDARKCLOUDCOVER,
            'CDLSPINNINGTOP': talib.CDLSPINNINGTOP,
            'CDL3INSIDE': talib.CDL3INSIDE,
        }

    async def analyze(self, data: Dict[str, Any]) -> Dict[str, Any]:
        open_prices = np.array(data['open'])
        high_prices = np.array(data['high'])
        low_prices = np.array(data['low'])
        close_prices = np.array(data['close'])

        results = {}

        for pattern_name, pattern_func in self.patterns.items():
            results[pattern_name] = pattern_func(open_prices, high_prices, low_prices, close_prices)

        # Identify the most recent pattern
        most_recent_pattern = None
        for i in range(len(close_prices) - 1, -1, -1):
            for pattern, values in results.items():
                if values[i] != 0:
                    most_recent_pattern = (pattern, values[i])
                    break
            if most_recent_pattern:
                break

        results['most_recent_pattern'] = most_recent_pattern

        return results