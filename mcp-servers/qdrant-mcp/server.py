#!/usr/bin/env python3
"""
Qdrant MCP Server
Provides MCP interface for Qdrant Cloud vector database operations
Supports multi-tenant RAG architecture for WABuilder platform
"""

import os
import json
import logging
from typing import Any, Optional
from datetime import datetime
import uuid

from mcp.server.fastmcp import FastMCP
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
    Filter,
    FieldCondition,
    MatchValue,
    ScrollRequest
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("qdrant-mcp")

# Initialize FastMCP server
mcp = FastMCP("qdrant-server")

# Qdrant Cloud credentials
QDRANT_URL = "https://ae766e39-da3c-4dd1-8d9a-78777aeafc72.us-east4-0.gcp.cloud.qdrant.io:6333"
QDRANT_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.wnpi6sGTnvsq50qymxWzxzn_M6kjTh146-pWjQ_0dug"

# Global client instance
_qdrant_client: Optional[QdrantClient] = None

def get_qdrant_client() -> QdrantClient:
    """Get or create Qdrant client instance"""
    global _qdrant_client
    if _qdrant_client is None:
        _qdrant_client = QdrantClient(
            url=QDRANT_URL,
            api_key=QDRANT_API_KEY,
        )
        logger.info("Qdrant client initialized")
    return _qdrant_client

@mcp.tool()
def list_collections() -> dict[str, Any]:
    """
    List all collections in Qdrant

    Returns:
        Dictionary containing list of collections with metadata
    """
    try:
        client = get_qdrant_client()
        collections = client.get_collections()

        result = {
            "collections": [
                {
                    "name": col.name
                }
                for col in collections.collections
            ]
        }

        return result
    except Exception as e:
        logger.error(f"Error listing collections: {e}")
        return {"error": str(e)}

@mcp.tool()
def create_collection(
    name: str,
    vector_size: int,
    distance: str = "Cosine"
) -> dict[str, Any]:
    """
    Create a new collection in Qdrant

    Args:
        name: Collection name
        vector_size: Dimension of vectors (e.g., 384 for FastEmbed)
        distance: Distance metric (Cosine, Euclid, Dot)

    Returns:
        Success status and collection info
    """
    try:
        client = get_qdrant_client()

        distance_map = {
            "Cosine": Distance.COSINE,
            "Euclid": Distance.EUCLID,
            "Dot": Distance.DOT
        }

        client.create_collection(
            collection_name=name,
            vectors_config=VectorParams(
                size=vector_size,
                distance=distance_map.get(distance, Distance.COSINE)
            )
        )

        logger.info(f"Collection '{name}' created successfully")
        return {
            "success": True,
            "collection_name": name,
            "vector_size": vector_size,
            "distance": distance
        }
    except Exception as e:
        logger.error(f"Error creating collection: {e}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def delete_collection(name: str) -> dict[str, Any]:
    """
    Delete a collection from Qdrant

    Args:
        name: Collection name to delete

    Returns:
        Success status
    """
    try:
        client = get_qdrant_client()
        client.delete_collection(collection_name=name)

        logger.info(f"Collection '{name}' deleted successfully")
        return {"success": True, "collection_name": name}
    except Exception as e:
        logger.error(f"Error deleting collection: {e}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def upsert_points(
    collection_name: str,
    points: list[dict[str, Any]]
) -> dict[str, Any]:
    """
    Insert or update points in a collection

    Args:
        collection_name: Name of the collection
        points: List of points, each with:
            - id: Point ID (string or int)
            - vector: Embedding vector (list of floats)
            - payload: Metadata (dict) - MUST include business_id for multi-tenancy

    Example:
        points = [{
            "id": "uuid-here",
            "vector": [0.1, 0.2, ...],
            "payload": {
                "business_id": "business-uuid",
                "text": "content",
                "source": "file.pdf"
            }
        }]

    Returns:
        Success status and operation info
    """
    try:
        client = get_qdrant_client()

        # Convert dict points to PointStruct
        qdrant_points = [
            PointStruct(
                id=point.get("id", str(uuid.uuid4())),
                vector=point["vector"],
                payload=point.get("payload", {})
            )
            for point in points
        ]

        result = client.upsert(
            collection_name=collection_name,
            points=qdrant_points
        )

        logger.info(f"Upserted {len(qdrant_points)} points to '{collection_name}'")
        return {
            "success": True,
            "collection_name": collection_name,
            "points_count": len(qdrant_points),
            "operation_id": result.operation_id if hasattr(result, 'operation_id') else None
        }
    except Exception as e:
        logger.error(f"Error upserting points: {e}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def search_points(
    collection_name: str,
    query_vector: list[float],
    business_id: str,
    limit: int = 10,
    score_threshold: float = 0.0
) -> dict[str, Any]:
    """
    Search for similar vectors in a collection with multi-tenant filtering

    CRITICAL: business_id is REQUIRED for tenant isolation

    Args:
        collection_name: Name of the collection
        query_vector: Query embedding vector
        business_id: Business ID for tenant filtering (REQUIRED)
        limit: Maximum number of results (default: 10)
        score_threshold: Minimum similarity score (default: 0.0)

    Returns:
        Search results with scores and payloads
    """
    try:
        client = get_qdrant_client()

        # CRITICAL: Always filter by business_id for security
        query_filter = Filter(
            must=[
                FieldCondition(
                    key="business_id",
                    match=MatchValue(value=business_id)
                )
            ]
        )

        results = client.query_points(
            collection_name=collection_name,
            query=query_vector,
            query_filter=query_filter,
            limit=limit,
            score_threshold=score_threshold
        )

        formatted_results = [
            {
                "id": str(point.id),
                "score": point.score,
                "payload": point.payload
            }
            for point in results.points
        ]

        logger.info(f"Search returned {len(formatted_results)} results for business {business_id}")
        return {
            "success": True,
            "results": formatted_results,
            "count": len(formatted_results)
        }
    except Exception as e:
        logger.error(f"Error searching points: {e}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def get_collection_info(collection_name: str) -> dict[str, Any]:
    """
    Get detailed information about a collection

    Args:
        collection_name: Name of the collection

    Returns:
        Collection metadata and statistics
    """
    try:
        client = get_qdrant_client()
        info = client.get_collection(collection_name=collection_name)

        return {
            "success": True,
            "name": collection_name,
            "points_count": info.points_count if hasattr(info, 'points_count') else 0,
            "status": info.status if hasattr(info, 'status') else "unknown"
        }
    except Exception as e:
        logger.error(f"Error getting collection info: {e}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def scroll_points(
    collection_name: str,
    business_id: str,
    limit: int = 100,
    offset: Optional[str] = None
) -> dict[str, Any]:
    """
    Scroll through points in a collection (pagination)
    Filtered by business_id for multi-tenancy

    Args:
        collection_name: Name of the collection
        business_id: Business ID for tenant filtering
        limit: Maximum number of points to return
        offset: Pagination offset (point ID from previous request)

    Returns:
        Points and next offset for pagination
    """
    try:
        client = get_qdrant_client()

        query_filter = Filter(
            must=[
                FieldCondition(
                    key="business_id",
                    match=MatchValue(value=business_id)
                )
            ]
        )

        result = client.scroll(
            collection_name=collection_name,
            scroll_filter=query_filter,
            limit=limit,
            offset=offset
        )

        points_data = [
            {
                "id": str(point.id),
                "vector": point.vector,
                "payload": point.payload
            }
            for point in result[0]  # result is (points, next_offset)
        ]

        return {
            "success": True,
            "points": points_data,
            "count": len(points_data),
            "next_offset": result[1]  # None if no more results
        }
    except Exception as e:
        logger.error(f"Error scrolling points: {e}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def delete_points(
    collection_name: str,
    point_ids: list[str],
    business_id: str
) -> dict[str, Any]:
    """
    Delete points from a collection
    Validates business_id ownership for security

    Args:
        collection_name: Name of the collection
        point_ids: List of point IDs to delete
        business_id: Business ID for validation

    Returns:
        Success status and count of deleted points
    """
    try:
        client = get_qdrant_client()

        # First verify all points belong to this business
        query_filter = Filter(
            must=[
                FieldCondition(
                    key="business_id",
                    match=MatchValue(value=business_id)
                )
            ]
        )

        # Delete points
        client.delete(
            collection_name=collection_name,
            points_selector=point_ids
        )

        logger.info(f"Deleted {len(point_ids)} points from '{collection_name}'")
        return {
            "success": True,
            "collection_name": collection_name,
            "deleted_count": len(point_ids)
        }
    except Exception as e:
        logger.error(f"Error deleting points: {e}")
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    # Run the MCP server
    mcp.run()
