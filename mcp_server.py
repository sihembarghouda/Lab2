# mcp_server.py
from fastmcp import FastMCP
from typing import List
from main import list_products as api_list_products, get_product as api_get_product

mcp = FastMCP(name="Product Catalog MCP Server")

# wrapper: fastmcp tools should be simple functions
@mcp.tool()
def list_products() -> List[dict]:
    """List all products."""
    # appelle la fonction du module main (qui utilise la DB)
    return api_list_products()

@mcp.tool()
def get_product(product_id: int) -> dict:
    """Get a product by id."""
    return api_get_product(product_id)

if __name__ == "__main__":
    mcp.run(host="127.0.0.1", port=8001)
