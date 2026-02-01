# Qdrant MCP Server

MCP (Model Context Protocol) server for Qdrant Cloud vector database operations.

## Features

- **Multi-tenant Support**: Built-in business_id filtering for secure tenant isolation
- **Collection Management**: Create, list, delete collections
- **Vector Operations**: Upsert, search, scroll, delete points
- **Security**: Enforced business_id filtering on all queries
- **WABuilder Integration**: Designed for the WABuilder platform architecture

## Installation

```bash
cd mcp-servers/qdrant-mcp
pip install -r requirements.txt
```

## Configuration

The server is pre-configured with Qdrant Cloud credentials:
- URL: `https://ae766e39-da3c-4dd1-8d9a-78777aeafc72.us-east4-0.gcp.cloud.qdrant.io:6333`
- API Key: Embedded in server.py

For production, move credentials to environment variables:
```bash
export QDRANT_URL="your-qdrant-url"
export QDRANT_API_KEY="your-api-key"
```

## Usage

### Running the Server

```bash
python server.py
```

### Available Tools

1. **list_collections()** - List all collections
2. **create_collection(name, vector_size, distance)** - Create new collection
3. **delete_collection(name)** - Delete collection
4. **get_collection_info(collection_name)** - Get collection details
5. **upsert_points(collection_name, points)** - Insert/update vectors
6. **search_points(collection_name, query_vector, business_id, limit, score_threshold)** - Search vectors
7. **scroll_points(collection_name, business_id, limit, offset)** - Paginate through points
8. **delete_points(collection_name, point_ids, business_id)** - Delete specific points

### Example: Creating WABuilder Knowledge Base

```python
# 1. Create collection
create_collection(
    name="wab_knowledge_base",
    vector_size=384,  # FastEmbed all-MiniLM-L6-v2
    distance="Cosine"
)

# 2. Upsert business knowledge
upsert_points(
    collection_name="wab_knowledge_base",
    points=[{
        "id": "point-uuid",
        "vector": [0.1, 0.2, ...],  # From gpu-ai embeddings_generate
        "payload": {
            "business_id": "business-uuid",
            "tenant_id": "business",
            "content_type": "faq",
            "text": "Business information here",
            "source": "knowledge.pdf",
            "timestamp": "2026-01-31T12:00:00Z"
        }
    }]
)

# 3. Search with tenant isolation
search_points(
    collection_name="wab_knowledge_base",
    query_vector=[0.15, 0.25, ...],  # Query embedding
    business_id="business-uuid",  # REQUIRED for security
    limit=5
)
```

## Multi-Tenancy Architecture

### Tenant Isolation
All search and scroll operations **require** a `business_id` parameter. This ensures:
- Each business only accesses their own data
- No cross-tenant data leakage
- Automatic security at the query level

### Payload Structure
```json
{
  "business_id": "uuid",          // REQUIRED - Tenant identifier
  "tenant_id": "business",         // Tenant type
  "content_type": "faq|product|...",
  "text": "Content text",
  "source": "source_file.pdf",
  "timestamp": "2026-01-31T12:00:00Z",
  "metadata": {}                   // Additional metadata
}
```

## Integration with WABuilder Stack

### MCP Server Chain
```
WABuilder Platform
    ↓
gpu-ai MCP ──→ Generate embeddings
    ↓
qdrant MCP ──→ Store/search vectors
    ↓
minio MCP ──→ Store original files
    ↓
langfuse ──→ Track costs/performance
```

### Workflow Example
1. **Document Upload**: Business uploads PDF via WhatsApp
2. **Processing**: Docling extracts text/images
3. **Embedding**: gpu-ai generates vectors (384d FastEmbed)
4. **Storage**:
   - Vectors → qdrant MCP (with business_id)
   - Files → minio MCP
   - Metadata → postgres MCP
5. **Query**: End user asks question
6. **RAG**:
   - Question → gpu-ai embedding
   - Search → qdrant MCP (filtered by business_id)
   - Context + Question → gpu-ai LLM
   - Response → User via WhatsApp

## Security Considerations

1. **Always Filter**: Never query without business_id filter
2. **Validate Ownership**: Verify business_id before delete operations
3. **Rate Limiting**: Implement per-tenant rate limits
4. **Storage Quotas**: Track and enforce per-business limits
5. **Audit Logging**: Log all operations with business_id

## Testing

See `test_qdrant_connection.py` for connection and operation tests.

```bash
python test_qdrant_connection.py
```

## Production Deployment

1. Move credentials to environment variables
2. Add rate limiting per business_id
3. Implement storage quota tracking
4. Set up monitoring and alerting
5. Configure backup strategy
6. Enable SSL/TLS verification

## License

Proprietary - WABuilder Platform
