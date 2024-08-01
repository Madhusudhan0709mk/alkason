from typing import Dict, Any, List
import numpy as np
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from infrastructure.logging_service import LoggingService
from datetime import datetime

class EnhancedVectorDatabase:
    def __init__(self, config: Dict[str, Any], logging_service: LoggingService):
        self.config = config
        self.logging_service = logging_service
        self.client = None
        self.collection_name = "market_patterns"
        self.version = 1

    async def initialize(self):
        try:
            self.client = QdrantClient(
                host=self.config['vector_db']['host'],
                port=self.config['vector_db']['port']
            )
            await self.logging_service.log_info("Enhanced Vector Database initialized successfully")
        except Exception as e:
            await self.logging_service.log_error(f"Error initializing Enhanced Vector Database: {str(e)}")
            raise

    async def create_collection(self, dimension: int):
        try:
            self.client.recreate_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=dimension, distance=Distance.COSINE)
            )
            await self.logging_service.log_info(f"Collection '{self.collection_name}' created successfully")
        except Exception as e:
            await self.logging_service.log_error(f"Error creating collection: {str(e)}")
            raise

    async def store_vector(self, vector: np.ndarray, metadata: Dict[str, Any]):
        try:
            point_id = f"{metadata.get('symbol')}_{metadata.get('timestamp')}_{self.version}"
            self.client.upsert(
                collection_name=self.collection_name,
                points=[
                    {
                        'id': point_id,
                        'vector': vector.tolist(),
                        'payload': {
                            **metadata,
                            'version': self.version,
                            'created_at': datetime.now().isoformat()
                        }
                    }
                ]
            )
            await self.logging_service.log_info(f"Vector stored successfully: {point_id}")
        except Exception as e:
            await self.logging_service.log_error(f"Error storing vector: {str(e)}")
            raise

    async def query_similar_vectors(self, vector: np.ndarray, k: int) -> List[Dict[str, Any]]:
        try:
            results = self.client.search(
                collection_name=self.collection_name,
                query_vector=vector.tolist(),
                limit=k
            )
            return [{'id': hit.id, 'score': hit.score, 'metadata': hit.payload} for hit in results]
        except Exception as e:
            await self.logging_service.log_error(f"Error querying similar vectors: {str(e)}")
            raise

    async def update_metadata(self, vector_id: str, new_metadata: Dict[str, Any]):
        try:
            self.client.update_payload(
                collection_name=self.collection_name,
                points=[vector_id],
                payload=new_metadata
            )
            await self.logging_service.log_info(f"Metadata updated successfully for vector: {vector_id}")
        except Exception as e:
            await self.logging_service.log_error(f"Error updating metadata: {str(e)}")
            raise

    async def create_snapshot(self, snapshot_name: str):
        try:
            self.client.create_snapshot(
                collection_name=self.collection_name,
                snapshot_name=snapshot_name
            )
            await self.logging_service.log_info(f"Snapshot created successfully: {snapshot_name}")
        except Exception as e:
            await self.logging_service.log_error(f"Error creating snapshot: {str(e)}")
            raise

    async def close(self):
        if self.client:
            self.client.close()
            await self.logging_service.log_info("Vector database connection closed")