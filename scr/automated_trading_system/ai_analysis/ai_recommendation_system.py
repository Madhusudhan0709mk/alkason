# File: ai_analysis/ai_recommendation_system.py

from typing import Dict, Any, List
from .ai_provider_factory import AIProviderFactory, AIProvider

class AIRecommendationSystem:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.ai_providers: Dict[str, AIProvider] = {}

    async def initialize(self):
        for provider_config in self.config.get('ai_providers', []):
            provider = AIProviderFactory.create(provider_config['name'], provider_config)
            self.ai_providers[provider_config['name']] = provider

    async def get_recommendations(self, data: Dict[str, Any]) -> Dict[str, Any]:
        recommendations = {}
        for provider_name, provider in self.ai_providers.items():
            recommendations[provider_name] = await provider.generate_recommendation(data)
        return recommendations

    def aggregate_recommendations(self, recommendations: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        actions = [rec['action'] for rec in recommendations.values()]
        confidences = [rec['confidence'] for rec in recommendations.values()]
        
        aggregated_action = max(set(actions), key=actions.count)
        aggregated_confidence = sum(confidences) / len(confidences)
        
        target_prices = [rec['target_price'] for rec in recommendations.values() if rec['target_price'] > 0]
        stop_losses = [rec['stop_loss'] for rec in recommendations.values() if rec['stop_loss'] > 0]
        
        aggregated_target_price = sum(target_prices) / len(target_prices) if target_prices else 0
        aggregated_stop_loss = sum(stop_losses) / len(stop_losses) if stop_losses else 0
        
        aggregated_reasoning = "; ".join([f"{provider}: {rec['reasoning']}" for provider, rec in recommendations.items()])
        
        return {
            'action': aggregated_action,
            'confidence': aggregated_confidence,
            'target_price': aggregated_target_price,
            'stop_loss': aggregated_stop_loss,
            'reasoning': aggregated_reasoning,
            'individual_recommendations': recommendations
        }