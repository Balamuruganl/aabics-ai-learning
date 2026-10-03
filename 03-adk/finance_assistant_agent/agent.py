from google.adk.agents import LlmAgent
from typing import Dict
from google.adk.tools.agent_tool import AgentTool
from investment_plan_agent.agent import investment_plan_agent

def get_user_personal_finance_details() -> Dict:
    """
        Gets users personal finance details like salary, expense and savings capacity.
    """
    return {
        "salary": 50000,
        "expense": {
            "EMI_Expense":25000,
            "Essentials":5000,
            "Entertainment": 5000,
            "Shopping and Travel":5000
        },
        "savings":10000
    }

finance_assistance_agent = LlmAgent(
    name="finance_assistance_agent",
    description="An agent that provides financial assistance and advice.",
    model="gemini-3.5-flash-lite",
    instruction="""
You are a financial assistance agent. Your task is to provide financial advice and assistance to users based 
on their queries. You should provide accurate and helpful information related to financial planning, 
investment strategies, budgeting
""",
    tools=[AgentTool(investment_plan_agent),  get_user_personal_finance_details]
)

root_agent = finance_assistance_agent

