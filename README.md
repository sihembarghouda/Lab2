# Lab: Building an AI-Ready Product Catalog with FastAPI and MCP

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![MCP](https://img.shields.io/badge/MCP-FastMCP-orange.svg)](https://github.com/jlowin/fastmcp)

## 📋 Table of Contents
- [Objective](#objective)
- [Prerequisites](#prerequisites)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Part 1: FastAPI Product Catalog API](#part-1-fastapi-product-catalog-api)
- [Part 2: MCP Server Integration](#part-2-mcp-server-integration)
- [Testing](#testing)
- [Docker Deployment](#docker-deployment)
- [AI Integration with Claude Desktop](#ai-integration-with-claude-desktop)
- [API Documentation](#api-documentation)
- [Troubleshooting](#troubleshooting)
- [Extensions & Next Steps](#extensions--next-steps)

## 🎯 Objective

In this lab, you will create a product catalog API using FastAPI and transform it into an AI-accessible service using the Model Context Protocol (MCP) with FastMCP. The lab demonstrates how to:

1. **Part 1**: Build and test a FastAPI-based product catalog API with PostgreSQL database
2. **Part 2**: Create an MCP server to expose your API as AI-callable tools

**Duration**: Approximately 90 minutes

## 📚 Prerequisites

- **Python 3.10+** installed
- Basic understanding of Python, REST APIs, and JSON
- Familiarity with terminal commands and virtual environments
- **Required packages**: `fastapi[all]`, `fastmcp`, `uvicorn`, `sqlalchemy`, `psycopg2-binary`
- **Optional**: Claude Desktop for testing AI tool calls (free tier sufficient)
- Code editor (e.g., VS Code)
- Docker and Docker Compose (for containerized deployment)

## 📁 Project Structure

```
product-catalog-lab/
├── README.md                 # This file
├── main.py                   # FastAPI application
├── mcp_server.py            # MCP server implementation
├── models.py                # SQLAlchemy models
├── database.py              # Database configuration
├── create_tables.py         # Database initialization script
├── requirements.txt         # Python dependencies
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Multi-container setup
├── openapi.json           # Generated OpenAPI schema
├── step1.txt              # Part 1 instructions
├── step2.txt              # Part 2 instructions
└── __pycache__/           # Python cache files
```

## 🚀 Installation

### Step 1: Set Up Your Environment

1. **Create and navigate to project directory**:
```bash
mkdir product-catalog-lab
cd product-catalog-lab
```

2. **Set up virtual environment**:
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux  
source venv/bin/activate
```

3. **Install required packages**:
```bash
pip install -r requirements.txt
```

**Alternative with uv**:
```bash
uv add fastapi[all] uvicorn fastmcp sqlalchemy psycopg2-binary
```

### Step 2: Database Setup

1. **Start PostgreSQL with Docker**:
```bash
docker-compose up -d db
```

2. **Initialize database tables**:
```bash
python create_tables.py
```

## 🏗️ Part 1: FastAPI Product Catalog API

### Features

- **RESTful API** with FastAPI framework
- **PostgreSQL database** integration with SQLAlchemy ORM
- **Pydantic models** for data validation
- **Automatic API documentation** with Swagger UI
- **CRUD operations** for product management

### Available Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/products` | List all products |
| GET | `/products/{id}` | Get product by ID |
| POST | `/products` | Create new product |

### Running the FastAPI Server

```bash
uvicorn main:app --host localhost --port 8000 --reload
```

**Access points**:
- API: http://localhost:8000
- Interactive docs: http://localhost:8000/docs
- OpenAPI schema: http://localhost:8000/openapi.json

### Testing the API

**List all products**:
```bash
curl http://localhost:8000/products
```

**Get specific product**:
```bash
curl http://localhost:8000/products/1
```

**Create new product**:
```bash
curl -X POST "http://localhost:8000/products" \
     -H "Content-Type: application/json" \
     -d '{"id": 4, "name": "Monitor", "price": 299.99, "description": "4K Display"}'
```

## 🤖 Part 2: MCP Server Integration

### What is MCP?

The Model Context Protocol (MCP) enables AI assistants to securely connect to external data sources and tools. FastMCP automatically converts your FastAPI endpoints into AI-callable tools.

### Running the MCP Server

1. **Keep FastAPI server running** on port 8000
2. **Start MCP server** in new terminal:
```bash
python mcp_server.py
```

The MCP server runs on port 8001 and exposes your API endpoints as AI tools.

### MCP Tools Available

- `list_products()`: Get all products from catalog
- `get_product(product_id)`: Retrieve specific product details

## 🧪 Testing

### Manual API Testing

**Using curl**:
```bash
# Test products endpoint
curl http://localhost:8000/products

# Test specific product
curl http://localhost:8000/products/1

# Test non-existent product (should return 404)
curl http://localhost:8000/products/999
```

**Using Swagger UI**:
1. Open http://localhost:8000/docs
2. Test both endpoints interactively
3. View request/response schemas

### Testing Database Integration

```bash
# Check if tables were created
python -c "from database import engine; from sqlalchemy import inspect; print(inspect(engine).get_table_names())"
```

## 🐳 Docker Deployment

### Option 1: Docker Compose (Recommended)

**Start all services**:
```bash
docker-compose up -d
```

**Services included**:
- PostgreSQL database (port 5432)
- FastAPI application (port 8000)

### Option 2: Manual Docker Build

**Build and run**:
```bash
docker build -t product-catalog .
docker run -p 8000:8000 product-catalog
```

## 🎯 AI Integration with Claude Desktop

### Setup Claude Desktop

1. **Install Claude Desktop** (if not installed)
2. **Configure MCP server** in `claude-desktop-config.json`:

```json
{
  "mcpServers": {
    "product-catalog": {
      "command": "C:\\Users\\zeine\\product-catalog-lab\\venv\\Scripts\\python.exe",
      "args": ["C:\\Users\\zeine\\product-catalog-lab\\mcp_server.py"]
    }
  }
}
```

3. **Restart Claude Desktop**
4. **Enable tools** in new chat: Search and tools > Select "product-catalog"

### Example AI Interactions

**Query**: "List all products in the catalog"
**Expected**: Claude calls `list_products_tool` and displays formatted product list

**Query**: "What is product with ID 2?"
**Expected**: Claude calls `get_product_tool` with ID 2 and shows product details

## 📖 API Documentation

### Product Model

```python
class Product(BaseModel):
    id: int                           # Unique identifier
    name: str                        # Product name
    price: float                     # Product price
    description: Optional[str]       # Optional description
```

### Response Examples

**GET /products**:
```json
[
  {
    "id": 1,
    "name": "Laptop",
    "price": 999.99,
    "description": "High-end gaming laptop"
  },
  {
    "id": 2,
    "name": "Wireless Mouse",
    "price": 29.99,
    "description": "Ergonomic wireless mouse"
  }
]
```

**GET /products/{id}**:
```json
{
  "id": 1,
  "name": "Laptop",
  "price": 999.99,
  "description": "High-end gaming laptop"
}
```

## 🔧 Troubleshooting

### Common Issues

**Database Connection Error**:
```bash
# Check if PostgreSQL is running
docker ps

# Restart database
docker-compose restart db
```

**Import Errors in MCP Server**:
```bash
# Ensure FastAPI server is running first
# Check Python path configuration in mcp_server.py
```

**Port Already in Use**:
```bash
# Kill process on port 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Debugging Tips

1. **Check logs**: Both FastAPI and MCP servers provide detailed console output
2. **Verify database**: Use pgAdmin or psql to inspect database contents
3. **Test endpoints**: Use Swagger UI at http://localhost:8000/docs
4. **Validate MCP**: Check Claude Desktop developer console for MCP errors

## 🚀 Extensions & Next Steps

### Immediate Enhancements

1. **Add authentication**: Implement JWT or API key authentication
2. **Add more endpoints**: PUT, DELETE operations for complete CRUD
3. **Data validation**: Enhanced Pydantic models with constraints
4. **Error handling**: Custom exception handlers and detailed error responses

### Advanced Features

1. **Database migrations**: Use Alembic for schema versioning
2. **Caching**: Implement Redis for improved performance  
3. **Testing suite**: Add pytest with fixtures and mocks
4. **API versioning**: Support multiple API versions
5. **Rate limiting**: Implement request throttling
6. **Monitoring**: Add logging, metrics, and health checks

### Production Deployment

1. **Environment variables**: Externalize configuration
2. **Security hardening**: HTTPS, CORS, security headers
3. **Container orchestration**: Kubernetes deployment
4. **CI/CD pipeline**: Automated testing and deployment
5. **Load balancing**: Multiple instance deployment

### AI Integration Extensions

1. **Natural language queries**: Add semantic search capabilities  
2. **Batch operations**: AI-driven bulk product management
3. **Recommendation engine**: AI-powered product suggestions
4. **Inventory management**: Stock level monitoring and alerts

## 📝 Submission Requirements

Submit the following files with screenshots:

**Required Files**:
- `main.py` - FastAPI application
- `mcp_server.py` - MCP server implementation  
- `models.py` - Database models
- `database.py` - Database configuration

**Screenshots**:
1. Swagger UI showing all FastAPI endpoints
2. Claude Desktop tool call outputs for `list_products_tool`
3. Claude Desktop tool call outputs for `get_product_tool`
4. Database content showing created products

## 👤 Author

**By Wahid Hamdi**

---

## 🤔 Reflection Questions

1. **How does Pydantic ensure data validation in API responses?**
2. **What happens when you send an invalid product_id (e.g., string instead of integer)?**
3. **How does FastMCP use your FastAPI app's OpenAPI schema to create tools?**
4. **What benefits do the @mcp.tool decorators provide for AI interactions?**
5. **How would you secure the MCP server for production use?**

---

**Happy coding! 🚀**
