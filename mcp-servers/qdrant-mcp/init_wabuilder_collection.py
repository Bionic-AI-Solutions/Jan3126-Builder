#!/usr/bin/env python3
"""
Initialize WABuilder knowledge base collection in Qdrant Cloud
Sets up the multi-tenant vector database for the platform
"""

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
import sys

def init_collection():
    """Initialize wab_knowledge_base collection"""

    print("🚀 Initializing WABuilder Knowledge Base Collection\n")

    try:
        # Connect to Qdrant Cloud
        client = QdrantClient(
            url="https://ae766e39-da3c-4dd1-8d9a-78777aeafc72.us-east4-0.gcp.cloud.qdrant.io:6333",
            api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.wnpi6sGTnvsq50qymxWzxzn_M6kjTh146-pWjQ_0dug",
        )

        collection_name = "wab_knowledge_base"

        # Check if collection already exists
        collections = client.get_collections()
        existing_names = [col.name for col in collections.collections]

        if collection_name in existing_names:
            print(f"⚠️  Collection '{collection_name}' already exists")
            print("   Skipping creation to preserve existing data")
            print("\n   To recreate, first delete the collection:")
            print(f"   client.delete_collection('{collection_name}')")
            return True

        # Create collection
        # Vector size: 384 (FastEmbed all-MiniLM-L6-v2)
        # Distance: Cosine (best for semantic similarity)
        print("📦 Creating collection:")
        print(f"   Name: {collection_name}")
        print(f"   Vector size: 384 (FastEmbed all-MiniLM-L6-v2)")
        print(f"   Distance metric: Cosine")

        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(
                size=384,
                distance=Distance.COSINE
            )
        )

        print(f"\n✅ Collection '{collection_name}' created successfully!")

        # Verify
        info = client.get_collection(collection_name=collection_name)
        print(f"\n📊 Collection Info:")
        print(f"   Status: {info.status}")
        print(f"   Points: {info.points_count}")

        print("\n🎯 Multi-Tenant Architecture Notes:")
        print("   - Each business isolated via business_id payload field")
        print("   - ALL queries MUST filter by business_id for security")
        print("   - Payload structure:")
        print("     {")
        print('       "business_id": "uuid",         // REQUIRED')
        print('       "tenant_id": "business",')
        print('       "content_type": "faq|product|...",')
        print('       "text": "...",')
        print('       "source": "file.pdf",')
        print('       "timestamp": "ISO-8601",')
        print('       "metadata": {...}')
        print("     }")

        print("\n✅ WABuilder knowledge base is ready for use!")

        return True

    except Exception as e:
        print(f"\n❌ Initialization failed: {str(e)}")
        return False

if __name__ == "__main__":
    success = init_collection()
    sys.exit(0 if success else 1)
