# File: decision_making/pattern_matching.py

from typing import Dict, Any, List
import numpy as np
from data.vector_database import VectorDatabase
from tslearn.preprocessing import TimeSeriesScalerMeanVariance
from tslearn.piecewise import SymbolicAggregateApproximation
from infrastructure.logging_service import LoggingService

class PatternMatcher:
    def __init__(self, config: Dict[str, Any], vector_db: VectorDatabase, logging_service: LoggingService):
        self.config = config
        self.vector_db = vector_db
        self.logging_service = logging_service
        self.scaler = TimeSeriesScalerMeanVariance()
        self.sax = SymbolicAggregateApproximation(n_segments=10, alphabet_size_avg=5)

    async def find_similar_patterns(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        try:
            time_series = np.array(data['market_data']['close'][-100:])
            scaled_series = self.scaler.fit_transform(time_series.reshape(1, -1, 1))
            sax_repr = self.sax.fit_transform(scaled_series)
            
            similar_patterns = await self.vector_db.query_similar_vectors(sax_repr.flatten(), k=5)
            
            await self.logging_service.log_info(f"Found {len(similar_patterns)} similar patterns")
            return similar_patterns
        except Exception as e:
            await self.logging_service.log_error(f"Error in find_similar_patterns: {str(e)}")
            return []

    async def add_pattern(self, data: Dict[str, Any], outcome: str):
        try:
            time_series = np.array(data['market_data']['close'][-100:])
            scaled_series = self.scaler.fit_transform(time_series.reshape(1, -1, 1))
            sax_repr = self.sax.fit_transform(scaled_series)
            
            await self.vector_db.store_vector(sax_repr.flatten(), {'outcome': outcome, 'data': data})
            await self.logging_service.log_info(f"Added new pattern with outcome: {outcome}")
        except Exception as e:
            await self.logging_service.log_error(f"Error in add_pattern: {str(e)}")