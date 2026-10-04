from google.adk.agents import LlmAgent
from google.adk.tools import ToolContext
from checkout_agent.agent import checkout_agent

def save_cart(tool_context: ToolContext,
              category: str,
              product: str,
              quantity: int,
              price:float):
    tool_context.state["category"] = category
    tool_context.state["product"] = product
    tool_context.state["quantity"] = quantity
    tool_context.state["price"] = price

catalog_agent = LlmAgent(
    name="catalog_agent",
    description="An agent that displays the list of products and their details",
    model="gemini-3.5-flash-lite",
    instruction="""
You are a catalog agent. Your task is to display the list of products and their details. 
Then get user's choice of product and quantity and save them using the save_cart function. 
The list of category and products is as follows:
1. Snacks
    - Curry leaves ladoo (100 gm : £1.50)
    - Kadalai mittai (100 gm : £2.50)
2. Masala powders
    - Sambar powder (100 gm : £1.50)
    - Quick Curry masala (100 gm : £2.50)
3. Mixes
    - Health Mix (100 gm : £1.50)
    - Ragi Mix (100 gm : £2.50)
Rules:
    1. The users could choose multiple products from different categories at once. 
       When it happens, you have to save the details of each product using the save_cart function.
       For example, if the user says multiple products, multiply the price of the product with the quantity and save it using the save_cart function.
                    if the user says 2 numbers of masala powders, you have to multiply the price of the product with the quantity and save it using the save_cart function.
    2. Using the user's choice, get the product name and quantity and calculate the price and save them using the save_cart function.
    3. If the user's choice is invalid, inform the user and ask them to choose again.
    4. Never answer the question yourself. 
    5. Once the details are collected, pass them to checkout-agent.
""",
    tools=[save_cart],
   sub_agents = [checkout_agent]
)