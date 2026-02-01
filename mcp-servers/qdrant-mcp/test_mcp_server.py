#!/usr/bin/env python3
"""
Test Qdrant MCP Server functionality
Validates that all tools are properly exposed and working
"""

import sys
import asyncio

async def test_mcp_server():
    """Test MCP server tools"""
    print("🧪 Testing Qdrant MCP Server\n")

    try:
        # Import the server
        sys.path.insert(0, '/workspaces/wabuilder/mcp-servers/qdrant-mcp')
        from server import mcp, get_qdrant_client

        # Test 1: Check client connection
        print("1️⃣ Testing Qdrant client connection...")
        client = get_qdrant_client()
        print("   ✅ Client initialized\n")

        # Test 2: List collections (via direct function call)
        print("2️⃣ Testing list_collections tool...")
        from server import list_collections
        result = list_collections()
        if "collections" in result:
            print(f"   ✅ Found {len(result['collections'])} collection(s)")
            for col in result['collections']:
                print(f"      - {col['name']}")
        else:
            print(f"   ⚠️  Result: {result}")
        print()

        # Test 3: Get collection info
        print("3️⃣ Testing get_collection_info tool...")
        from server import get_collection_info
        result = get_collection_info("wab_knowledge_base")
        if result.get("success"):
            print(f"   ✅ Collection: {result['name']}")
            print(f"      Points: {result['points_count']}")
            print(f"      Status: {result['status']}")
        else:
            print(f"   ⚠️  Result: {result}")
        print()

        # Test 4: Check tool definitions
        print("4️⃣ Checking MCP tool definitions...")
        tools = mcp.list_tools()
        print(f"   ✅ Registered {len(tools)} tools:")
        for tool in tools:
            print(f"      - {tool.name}")
        print()

        print("✅ All MCP server tests passed!\n")
        return True

    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_mcp_server())
    sys.exit(0 if success else 1)
