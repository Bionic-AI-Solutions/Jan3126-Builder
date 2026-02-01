#!/usr/bin/env python3
"""
Simple test of Qdrant MCP server tools
"""

import sys
sys.path.insert(0, '/workspaces/wabuilder/mcp-servers/qdrant-mcp')

from server import list_collections, get_collection_info, search_points
import uuid

print("🧪 Testing Qdrant MCP Server Tools\n")

# Test 1: List collections
print("1️⃣ list_collections()")
result = list_collections()
print(f"   Result: {result}\n")

# Test 2: Get collection info
print("2️⃣ get_collection_info('wab_knowledge_base')")
result = get_collection_info("wab_knowledge_base")
print(f"   Result: {result}\n")

# Test 3: Search (requires business_id)
print("3️⃣ search_points() - with test vector")
test_vector = [0.1] * 384
test_business_id = str(uuid.uuid4())
result = search_points(
    collection_name="wab_knowledge_base",
    query_vector=test_vector,
    business_id=test_business_id,  # Won't find anything since we don't have data for this ID
    limit=3
)
print(f"   Result: {result}")
print(f"   (Expected 0 results since business_id doesn't exist)\n")

print("✅ All tool tests completed!")
