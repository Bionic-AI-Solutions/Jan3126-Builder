#!/usr/bin/env python3
"""
Test Qdrant Cloud connection and MCP server functionality
"""

from qdrant_client import QdrantClient
import sys

def test_connection():
    """Test connection to Qdrant Cloud"""

    print("🔌 Testing Qdrant Cloud Connection\n")

    try:
        # Initialize client
        qdrant_client = QdrantClient(
            url="https://ae766e39-da3c-4dd1-8d9a-78777aeafc72.us-east4-0.gcp.cloud.qdrant.io:6333",
            api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.wnpi6sGTnvsq50qymxWzxzn_M6kjTh146-pWjQ_0dug",
        )

        print("✅ Client initialized successfully")

        # Get collections
        collections = qdrant_client.get_collections()

        print(f"\n📦 Collections ({len(collections.collections)}):")
        if collections.collections:
            for col in collections.collections:
                print(f"   - {col.name}")
                # Get detailed info for each collection
                try:
                    info = qdrant_client.get_collection(col.name)
                    print(f"     Points: {info.points_count}")
                    print(f"     Status: {info.status}")
                except:
                    pass
        else:
            print("   (No collections found)")

        print("\n✅ Connection test successful!")
        print("\nQdrant Cloud is ready for WABuilder platform integration.")

        return True

    except Exception as e:
        print(f"\n❌ Connection test failed: {str(e)}")
        print("\nPlease verify:")
        print("  1. Qdrant Cloud URL is correct")
        print("  2. API key is valid")
        print("  3. Network connectivity to Qdrant Cloud")
        return False

if __name__ == "__main__":
    success = test_connection()
    sys.exit(0 if success else 1)
