from typing import Dict, Any, List
import numpy as np
from tslearn.preprocessing import TimeSeriesScalerMeanVariance
from tslearn.piecewise import SymbolicAggregateApproximation
from sklearn.preprocessing import normalize
from .enhanced_vector_database import EnhancedVectorDatabase
from infrastructure.logging_service import LoggingService

class VectorDatabaseEnhancement:
    def __init__(self, vector_db: EnhancedVectorDatabase, config: Dict[str, Any], logging_service: LoggingService):
        self.vector_db = vector_db
        self.config = config
        self.logging_service = logging_service
        self.scaler = TimeSeriesScalerMeanVariance()
        self.sax = SymbolicAggregateApproximation(n_segments=10, alphabet_size_avg=5)

    async def enhance_database(self, new_data: Dict[str, Any]):
        try:
            time_series = new_data['time_series']
            time_series_reshaped = np.array(time_series).reshape(1, -1, 1)
            scaled_series = self.scaler.fit_transform(time_series_reshaped)
            sax_representation = self.sax.fit_transform(scaled_series)
            vector = normalize(sax_representation.reshape(1, -1))[0]
            
            metadata = {k: v for k, v in new_data.items() if k != 'time_series'}
            metadata['id'] = f"{new_data['symbol']}_{new_data['timestamp']}"
            
            await self.vector_db.store_vector(vector, metadata)
            await self.logging_service.log_info(f"Enhanced and stored vector for {metadata['id']}")
        except Exception as e:
            await self.logging_service.log_error(f"Error enhancing database: {str(e)}")
            raise

    async def find_similar_patterns(self, query_data: Dict[str, Any], k: int = 5) -> List[Dict[str, Any]]:
        try:
            query_series = query_data['time_series']
            query_series_reshaped = np.array(query_series).reshape(1, -1, 1)
            scaled_query = self.scaler.transform(query_series_reshaped)
            sax_query = self.sax.transform(scaled_query)
            query_vector = normalize(sax_query.reshape(1, -1))[0]
            
            similar_patterns = await self.vector_db.query_similar_vectors(query_vector, k)
            await self.logging_service.log_info(f"Found {len(similar_patterns)} similar patterns")
            return similar_patterns
        except Exception as e:
            await self.logging_service.log_error(f"Error finding similar patterns: {str(e)}")
            raise

    async def update_pattern(self, pattern_id: str, updated_data: Dict[str, Any]):
        try:
            await self.vector_db.update_metadata(pattern_id, updated_data)
            await self.logging_service.log_info(f"Updated pattern {pattern_id}")
        except Exception as e:
            await self.logging_service.log_error(f"Error updating pattern: {str(e)}")
            raise

    async def create_database_snapshot(self, snapshot_name: str):
        try:
            await self.vector_db.create_snapshot(snapshot_name)
            await self.logging_service.log_info(f"Created database snapshot: {snapshot_name}")
        except Exception as e:
            await self.logging_service.log_error(f"Error creating database snapshot: {str(e)}")
            raise