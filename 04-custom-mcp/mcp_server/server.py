import os
from typing import Any
import logging

import psycopg
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from psycopg.rows import dict_row

load_dotenv()

logging.basicConfig(level=logging.INFO)

mcp = FastMCP("organic-shop-server",
               host="127.0.0.1",
               port=8001,
              )

def get_db_connection():
    """Connect to PostgreSQL through the local Cloud SQL Auth Proxy."""
    return psycopg.connect(
        host=os.environ["DB_HOST"],
        port=int(os.getenv("DB_PORT", "5432")),
        dbname=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        row_factory=dict_row,
        connect_timeout=10,
    )

@mcp.tool()
def search_products(
    search_term: str = "",
    category: str = "",
    max_price: float | None = None,
    in_stock_only: bool = False,
    limit: int = 10,
) -> list[dict[str, Any]]:
    """Search organic shop products by name, ingredients, category,
    maximum price in INR, and stock availability.

    Returns product IDs, names, categories, prices in INR,
    pack sizes, and stock quantities.
    """
    if max_price is not None and max_price < 0:
        raise ValueError("Maximum price cannot be negative.")

    if not 1 <= limit <= 50:
        raise ValueError("Limit must be between 1 and 50.")

    conditions = ["is_active = TRUE"]
    params: list[Any] = []

    if search_term.strip():
        conditions.append(
            "(product_name ILIKE %s OR ingredients ILIKE %s)"
        )
        term = f"%{search_term.strip()}%"
        params.extend([term, term])

    if category.strip():
        conditions.append("category ILIKE %s")
        params.append(category.strip())

    if max_price is not None:
        conditions.append("price <= %s")
        params.append(max_price)

    if in_stock_only:
        conditions.append("stock_quantity > 0")

    sql = f"""
        SELECT product_id, product_name, category,
               ingredients, price, weight_grams, stock_quantity
        FROM products
        WHERE {" AND ".join(conditions)}
        ORDER BY price ASC, product_name ASC
        LIMIT %s
    """
    params.append(limit)

    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, params)
            rows = cursor.fetchall()

    # Convert Decimal prices into JSON-friendly numbers.
    return [
        {
            **dict(row),
            "price": float(row["price"]),
        }
        for row in rows
    ]


if __name__ == "__main__":
    logging.info("Starting Organic Shop MCP server")
    mcp.run(
        transport="streamable-http"
    )
    logging.info("MCP server stopped")