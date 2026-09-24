from langchain_core.tools import tool
from db import fetch_all, fetch_one
from weather_api import get_current_weather
from rag.rag_engine import search_text
from rules import assess_product

@tool
def weather_tool() -> dict:
    """Get current weather/environment data for the configured mall location."""
    return get_current_weather()

@tool
def product_lookup_tool(product_id: str) -> dict:
    """Read a product's requirements from Microsoft SQL Server."""
    row = fetch_one(
        "SELECT * FROM dbo.Products WHERE ProductID = :product_id",
        {"product_id": product_id},
    )
    return row or {"error": f"Product {product_id} was not found."}

@tool
def product_search_tool(query: str) -> list:
    """Search the SQL Server catalog by product, category, subcategory or SKU."""
    return fetch_all(
        """
        SELECT TOP 20 ProductID, SKU, ProductName, Category, SubCategory,
               Perishable, Hazardous, ExpiryDate, MinTempC, MaxTempC,
               MaxRelativeHumidity, LightSensitive, FreezeSensitive
        FROM dbo.Products
        WHERE ProductName LIKE :q
           OR Category LIKE :q
           OR SubCategory LIKE :q
           OR SKU LIKE :q
        ORDER BY Category, ProductName
        """,
        {"q": f"%{query}%"},
    )

@tool
def product_rag_tool(question: str) -> str:
    """Retrieve relevant product handling information from the PDF."""
    return search_text(question)

@tool
def transport_assessment_tool(product_id: str) -> dict:
    """Compare current environmental data with SQL product limits and expiry."""
    product = product_lookup_tool.invoke(product_id)
    if "error" in product:
        return product
    weather = weather_tool.invoke({})
    return assess_product(product, weather)
