from google.adk.agents import LlmAgent
from google.adk.tools import ToolContext

def save_shipping_address(tool_context: ToolContext,
              shipping_address: str,
              ):
    tool_context.state["shipping_address"] = shipping_address

checkout_agent = LlmAgent(
    name="checkout_agent",
    description="An agent that handles the checkout process for the products in the cart and displays the order summary",
    model="gemini-3.5-flash-lite",
    instruction="""
You are a checkout agent. Your task is to get the shipping address using the save_shipping_address tool

Workflow:
Follow these steps in EXACT order:
1. Ask the user for their shipping address.
2. Wait for the user's response.
3. Take the shipping address provided by the user and call the
   save_shipping_address tool with that exact address.
4. After the tool successfully saves the address, read the order information
   from state and display the order summary in the below format.

Your order will be shipped
{name} {email} {mobile?}
{category} {product} {quantity} {price}
{shipping_address?}
Rules:
    1. You should get the shipping address from the user and save it using the save_shipping_address tool.
    2. Then display the order summary in the above format using the information from the state.
    3. Read ONLY from state; do NOT invent random information that are not in state.
""",
    tools=[save_shipping_address]
)