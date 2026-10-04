from google.adk.agents import LlmAgent
from google.adk.tools import ToolContext
from catalog_agent.agent import catalog_agent

def save_user_info(tool_context: ToolContext,
                   name: str,
                   email: str,
                   mobile: str):

    tool_context.state["name"] = name
    tool_context.state["email"] = email
    tool_context.state["mobile"] = mobile


root_agent = LlmAgent(
    name="ecommerce_agent",
    description="An ecommerce agent that manages the ecommmerce workflow",
    model="gemini-3.5-flash-lite",
    instruction="""
You are an ecommerce agent. Your task is to manage the ecommerce workflow and provide assistance to users
Based on their queries. 

Roles: You should welcome the user and get their details like name, email and phone number. 
       Get the details one by one.
       Once you get the details, save them using the save_user_info function.
       You will have multiple sub agents to help you with the workflow. You should call the sub agents when needed.
       The sub agents are:
         1. catalog_agent to display the list of products and their details.
         2. checkout_agent to provide the summary of the order and the user details.

Rules:
    1. NEVER answer the question yourself. Always delegate to exactly one sub-agent.
    2. If the user's message clearly matches one category, immediately call that agent.
    3. If you are unsure, ask a short clarifying question instead of guessing.
    4. After a sub-agent responds, you may send that response back as-is to the user,
    without adding extra content.

""",
    tools=[save_user_info],
    sub_agents = [catalog_agent]
)
