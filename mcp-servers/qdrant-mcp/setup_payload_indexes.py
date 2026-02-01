#!/usr/bin/env python3
"""
Setup payload indexes for WABuilder knowledge base
Creates indexes for efficient multi-tenant filtering
"""

from qdrant_client import QdrantClient
from qdrant_client.models import PayloadSchemaType
import sys

def setup_indexes():
    """Create payload indexes for business_id and other frequently queried fields"""

    print("🔧 Setting up Qdrant Payload Indexes\n")

    try:
        # Connect to Qdrant Cloud
        client = QdrantClient(
            url="https://ae766e39-da3c-4dd1-8d9a-78777aeafc72.us-east4-0.gcp.cloud.qdrant.io:6333",
            api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.wnpi6sGTnvsq50qymxWzxzn_M6kjTh146-pWjQ_0dug",
        )

        collection_name = "wab_knowledge_base"

        # ===================================================================
        # Index 1: business_id (CRITICAL for multi-tenant filtering)
        # ===================================================================
        print("📊 Creating index: business_id (keyword)")
        print("   Purpose: Multi-tenant isolation and filtering")
        print("   Type: keyword (exact match)")

        client.create_payload_index(
            collection_name=collection_name,
            field_name="business_id",
            field_schema=PayloadSchemaType.KEYWORD
        )
        print("   ✅ Index created\n")

        # ===================================================================
        # Index 2: content_type (for filtering by document type)
        # ===================================================================
        print("📊 Creating index: content_type (keyword)")
        print("   Purpose: Filter by document type (faq, product, etc.)")
        print("   Type: keyword")

        client.create_payload_index(
            collection_name=collection_name,
            field_name="content_type",
            field_schema=PayloadSchemaType.KEYWORD
        )
        print("   ✅ Index created\n")

        # ===================================================================
        # Index 3: category (for categorical filtering)
        # ===================================================================
        print("📊 Creating index: category (keyword)")
        print("   Purpose: Filter by category (optional metadata)")
        print("   Type: keyword")

        client.create_payload_index(
            collection_name=collection_name,
            field_name="category",
            field_schema=PayloadSchemaType.KEYWORD
        )
        print("   ✅ Index created\n")

        # ===================================================================
        # Verify indexes
        # ===================================================================
        print("🔍 Verifying collection configuration...")
        info = client.get_collection(collection_name=collection_name)

        print(f"\n✅ Collection '{collection_name}' indexes configured:")
        print("   - business_id: keyword (multi-tenant filtering)")
        print("   - content_type: keyword (document type filtering)")
        print("   - category: keyword (category filtering)")
        print()
        print("🎯 Multi-tenant queries are now optimized!")
        print()

        return True

    except Exception as e:
        print(f"\n❌ Index setup failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = setup_indexes()
    sys.exit(0 if success else 1)
