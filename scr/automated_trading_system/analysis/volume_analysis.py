# File: analysis/volume_analysis.py

import numpy as np
import pandas as pd
import talib
from typing import Dict, Any

class VolumeAnalysis:
    def __init__(self, config: Dict[str, Any]):
        self.config = config

    async def analyze(self, data: Dict[str, Any]) -> Dict[str, Any]:
        df = pd.DataFrame(data['market_data'])
        
        results = {}
        
        # On-Balance Volume (OBV)
        results['OBV'] = talib.OBV(df['close'], df['volume'])

        # Volume Price Trend (VPT)
        results['VPT'] = self.calculate_vpt(df)

        # Volume Weighted Average Price (VWAP)
        results['VWAP'] = self.calculate_vwap(df)

        # Accumulation/Distribution Line (A/D Line)
        results['AD'] = talib.AD(df['high'], df['low'], df['close'], df['volume'])

        # Negative Volume Index (NVI) and Positive Volume Index (PVI)
        results['NVI'], results['PVI'] = self.calculate_nvi_pvi(df)

        # Money Flow Index (MFI)
        results['MFI'] = talib.MFI(df['high'], df['low'], df['close'], df['volume'])

        return results

    def calculate_vpt(self, df: pd.DataFrame) -> np.ndarray:
        vpt = (df['volume'] * ((df['close'] - df['close'].shift(1)) / df['close'].shift(1))).cumsum()
        return vpt.values

    def calculate_vwap(self, df: pd.DataFrame) -> np.ndarray:
        v = df['volume'].values
        tp = (df['high'] + df['low'] + df['close']) / 3
        return (tp * v).cumsum() / v.cumsum()

    def calculate_nvi_pvi(self, df: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
        nvi = 1000.0
        pvi = 1000.0
        nvi_list = [nvi]
        pvi_list = [pvi]
        for i in range(1, len(df)):
            if df['volume'].iloc[i] < df['volume'].iloc[i-1]:
                nvi *= (1.0 + (df['close'].iloc[i] - df['close'].iloc[i-1]) / df['close'].iloc[i-1])
            if df['volume'].iloc[i] > df['volume'].iloc[i-1]:
                pvi *= (1.0 + (df['close'].iloc[i] - df['close'].iloc[i-1]) / df['close'].iloc[i-1])
            nvi_list.append(nvi)
            pvi_list.append(pvi)
        return np.array(nvi_list), np.array(pvi_list)