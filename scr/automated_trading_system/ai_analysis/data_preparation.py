# File: ai_analysis/data_preparation.py

from typing import Dict, Any
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

class DataPreparation:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.scaler = MinMaxScaler()

    def prepare_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        df = pd.DataFrame(data['market_data'])
        df = self.normalize_data(df)
        df = self.engineer_features(df)
        
        prepared_data = {
            'market_data': df.to_dict(orient='list'),
            'technical_indicators': data['technical_indicators'],
            'sentiment_score': data['sentiment_score'],
            'intermarket_data': data['intermarket_data']
        }
        
        return prepared_data

    def normalize_data(self, df: pd.DataFrame) -> pd.DataFrame:
        columns_to_normalize = ['open', 'high', 'low', 'close', 'volume']
        df[columns_to_normalize] = self.scaler.fit_transform(df[columns_to_normalize])
        return df

    def engineer_features(self, df: pd.DataFrame) -> pd.DataFrame:
        df['returns'] = df['close'].pct_change()
        df['log_returns'] = np.log(df['close'] / df['close'].shift(1))
        df['volatility'] = df['returns'].rolling(window=20).std()
        return df