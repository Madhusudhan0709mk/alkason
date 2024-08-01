# File: analysis/continuous_improvement.py

from typing import Dict, Any, List
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

class ContinuousImprovement:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.model = RandomForestClassifier()
        self.historical_data = []

    async def analyze_and_improve(self, historical_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        self.historical_data.extend(historical_data)
        
        X = []
        y = []
        for trade in self.historical_data:
            features = self.extract_features(trade)
            X.append(features)
            y.append(1 if trade['outcome'] == 'success' else 0)

        X = np.array(X)
        y = np.array(y)

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        self.model.fit(X_train, y_train)
        accuracy = self.model.score(X_test, y_test)

        feature_importance = dict(zip(self.get_feature_names(), self.model.feature_importances_))

        return {
            'model_accuracy': accuracy,
            'feature_importance': feature_importance,
            'improvement_suggestions': self.generate_improvement_suggestions(feature_importance)
        }

    def extract_features(self, trade: Dict[str, Any]) -> List[float]:
        return [
            trade['technical_indicators']['RSI'],
            trade['technical_indicators']['MACD'],
            trade['sentiment_score'],
            trade['intermarket_correlation'],
            trade['pattern_strength']
        ]

    def get_feature_names(self) -> List[str]:
        return ['RSI', 'MACD', 'Sentiment', 'Intermarket Correlation', 'Pattern Strength']

    def generate_improvement_suggestions(self, feature_importance: Dict[str, float]) -> List[str]:
        suggestions = []
        for feature, importance in sorted(feature_importance.items(), key=lambda x: x[1], reverse=True):
            if importance > 0.2:
                suggestions.append(f"Consider giving more weight to {feature} in decision making.")
            elif importance < 0.05:
                suggestions.append(f"The impact of {feature} might be overestimated. Consider reducing its influence.")
        return suggestions