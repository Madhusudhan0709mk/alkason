# File: ai_analysis/ai_performance_tracker.py

from typing import Dict, Any
from datetime import datetime, timedelta

class AIPerformanceTracker:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.performance_data = {}

    async def track_performance(self, provider_name: str, recommendation: Dict[str, Any], actual_outcome: Dict[str, Any]):
        if provider_name not in self.performance_data:
            self.performance_data[provider_name] = []
        
        performance_entry = {
            "timestamp": datetime.now().isoformat(),
            "recommendation": recommendation,
            "actual_outcome": actual_outcome,
            "accuracy": self._calculate_accuracy(recommendation, actual_outcome)
        }
        
        self.performance_data[provider_name].append(performance_entry)
        
        # Prune old data if necessary
        max_entries = self.config.get("max_performance_entries", 1000)
        if len(self.performance_data[provider_name]) > max_entries:
            self.performance_data[provider_name] = self.performance_data[provider_name][-max_entries:]

    async def generate_performance_report(self) -> Dict[str, Any]:
        report = {}
        for provider, entries in self.performance_data.items():
            if entries:
                avg_accuracy = sum(entry["accuracy"] for entry in entries) / len(entries)
                report[provider] = {
                    "average_accuracy": avg_accuracy,
                    "total_recommendations": len(entries),
                    "last_24h_accuracy": self._calculate_recent_accuracy(entries, hours=24),
                    "last_7d_accuracy": self._calculate_recent_accuracy(entries, hours=168)
                }
        return report

    def _calculate_accuracy(self, recommendation: Dict[str, Any], actual_outcome: Dict[str, Any]) -> float:
        if recommendation['action'] == actual_outcome['action']:
            return 1.0
        elif recommendation['action'] == 'HOLD' or actual_outcome['action'] == 'HOLD':
            return 0.5
        else:
            return 0.0

    def _calculate_recent_accuracy(self, entries: List[Dict[str, Any]], hours: int) -> float:
        cutoff_time = datetime.now() - timedelta(hours=hours)
        recent_entries = [entry for entry in entries if datetime.fromisoformat(entry['timestamp']) > cutoff_time]
        if recent_entries:
            return sum(entry['accuracy'] for entry in recent_entries) / len(recent_entries)
        return 0.0