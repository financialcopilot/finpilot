import os
import json
import math
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from google.api_core.exceptions import ResourceExhausted

# Load environment variables from .env file
load_dotenv()

# --- NEW: API Key Management ---
# Load all keys from the .env file and split them into a list
API_KEYS = os.getenv("GOOGLE_API_KEYS", "").split(',')
if not all(API_KEYS) or API_KEYS == ['']:
    raise ValueError("GOOGLE_API_KEYS environment variable not set or is empty. Please check your .env file.")

# --- NEW: Resilient LLM Invoker with Key Cycling ---
async def invoke_llm_with_retry(prompt_template, input_data):
    """
    Tries to invoke a LangChain chain with a list of API keys.
    If a key is rate-limited (ResourceExhausted), it automatically retries with the next key.
    """
    for i, key in enumerate(API_KEYS):
        try:
            # Initialize a new LLM instance with the current key for this specific call
            llm = ChatGoogleGenerativeAI(
                model="gemini-1.5-flash-latest",
                temperature=0.7,
                google_api_key=key
            )
            
            # Build the full chain using the prompt and the new LLM instance
            chain = prompt_template | llm | StrOutputParser()
            
            print(f"--- Attempting API call with Key #{i + 1} ---")
            response = await chain.ainvoke(input_data)
            print(f"--- Key #{i + 1} succeeded. ---")
            return response # Success, so we return the response

        except ResourceExhausted:
            print(f"Warning: API Key #{i + 1} is rate-limited or exhausted. Trying next key...")
            if i == len(API_KEYS) - 1: # If this was the last key in the list
                print("Error: All API keys are exhausted.")
                raise # Re-raise the final exception if all keys have failed
        except Exception as e:
            # Handle other potential errors (e.g., an invalid key format)
            print(f"An unexpected error occurred with Key #{i + 1}: {e}")
            if i == len(API_KEYS) - 1:
                raise
    
    # This line should ideally not be reached, but is a fallback.
    raise Exception("All API keys failed to generate a response.")


# --- Agent 1: The Analyst ---
analyst_template = """
You are an expert financial analyst. Your role is to analyze a user's financial data and provide a structured, factual summary.
Identify potential red flags and key strengths based on the provided user data and market context. Do not give any advice.

USER DATA:
{user_data}

MARKET CONTEXT (Note: these are historical averages for projection):
{market_stats}

Analyze the data and provide a concise summary covering:
1.  *Financial Health Score:* A score out of 10 (e.g., 7/10).
2.  *Key Observations:* 3-4 bullet points on their savings rate, debt-to-income ratio, and asset composition.
3.  *Red Flags:* 1-2 bullet points on urgent issues (e.g., high-interest debt, low emergency savings).
4.  *Strengths:* 1-2 bullet points on what they are doing well.

Your entire output must be a single block of text, clearly formatted.
ANALYSIS:
"""
analyst_prompt = PromptTemplate(
    template=analyst_template,
    input_variables=["user_data", "market_stats"]
)

# --- Agent 2: The Strategist ---
strategist_template = """
You are a master financial strategist for the Indian market. You will receive an analysis from a financial analyst.
Your job is to first critique the analysis for accuracy and then create two distinct, high-level financial strategies based on it.
Pay close attention to the asset correlations provided in the analyst's summary to ensure proper diversification.

ANALYST'S SUMMARY (includes user data and market stats with correlations):
{analyst_summary}

Based on this analysis, devise two strategies:
1.  *Sentinel Plan (Safe & Steady):* A conservative plan focusing on debt reduction, building a strong emergency fund, and using low-risk, low-correlation investments for stability.
2.  *Voyager Plan (Growth-Oriented):* A more aggressive plan that accepts calculated market risk for potentially higher returns and faster goal achievement, while still being diversified.

For each plan, define the core philosophy and the primary action steps. Do not go into specific numerical projections yet.
STRATEGIES:
"""
strategist_prompt = PromptTemplate(
    template=strategist_template,
    input_variables=["analyst_summary"]
)

# --- Agent 3: The Writer ---
writer_template = """
You are a skilled financial writer. You will receive a user's data and two high-level strategies.
Your task is to synthesize all this information into a final, detailed, and user-friendly financial plan.
Calculate specific numbers for asset allocation percentages and projected goal timelines based on the strategies and user data.

USER DATA:
{user_data}

HIGH-LEVEL STRATEGIES:
{strategies}

Based on everything, create a complete financial plan.
Your entire response MUST be a single, valid JSON object, with no other text before or after it.
The JSON object should follow this exact structure:
{{
  "sentinel_plan": {{
    "summary": "A brief, encouraging summary of this safe plan.",
    "asset_allocation": {{ "equities": "X%", "bonds": "Y%", "commodities": "Z%", "cash": "A%" }},
    "projected_goal_timeline_years": {{ "User's Goal Name 1": "X", "User's Goal Name 2": "Y" }},
    "recommendations": ["Detailed recommendation 1", "Detailed recommendation 2", "Detailed recommendation 3"]
  }},
  "voyager_plan": {{
    "summary": "A brief, encouraging summary of this growth-oriented plan.",
    "asset_allocation": {{ "equities": "X%", "bonds": "Y%", "crypto": "Z%", "cash": "A%" }},
    "projected_goal_timeline_years": {{ "User's Goal Name 1": "X", "User's Goal Name 2": "Y" }},
    "recommendations": ["Detailed recommendation 1", "Detailed recommendation 2", "Detailed recommendation 3"]
  }}
}}
"""
writer_prompt = PromptTemplate(
    template=writer_template,
    input_variables=["user_data", "strategies"]
)

# --- The AI Assembly Line Chain ---
async def generate_plan_with_assembly_line(user_profile: dict):
    with open("market_stats.json", "r") as f:
        market_stats = json.load(f)

    analyst_input = {"user_data": json.dumps(user_profile), "market_stats": json.dumps(market_stats)}
    analyst_summary = await invoke_llm_with_retry(analyst_prompt, analyst_input)

    strategist_input = {"analyst_summary": analyst_summary}
    strategies = await invoke_llm_with_retry(strategist_prompt, strategist_input)

    writer_input = {"user_data": json.dumps(user_profile), "strategies": strategies}
    final_plan_str = await invoke_llm_with_retry(writer_prompt, writer_input)
    
    return final_plan_str

# --- Agent 4: The Economic Forecaster ---
forecaster_template = """
You are an expert economic forecaster for the Indian market. Your task is to generate 3 distinct, plausible economic scenarios for the next 5 years.
One scenario should be optimistic (a bull run), one pessimistic (a slowdown), and one mixed/neutral.

For EACH of the 3 scenarios, you MUST provide two things:
1. A short, creative 'narrative' paragraph describing the economic story.
2. A structured JSON object with these exact keys and estimated annual percentage values: {{"avg_equity_return": X, "avg_bond_return": Y, "avg_inflation": Z}}

Your entire response MUST be a single, valid JSON object, with no other text before or after it.
The JSON object should follow this exact structure:
{{
  "scenarios": [
    {{
      "name": "The Optimistic Scenario",
      "narrative": "A descriptive story of a booming economy...",
      "parameters": {{ "avg_equity_return": 18.0, "avg_bond_return": 7.5, "avg_inflation": 4.5 }}
    }},
    {{
      "name": "The Pessimistic Scenario",
      "narrative": "A descriptive story of a sluggish economy...",
      "parameters": {{ "avg_equity_return": 2.0, "avg_bond_return": 6.0, "avg_inflation": 8.0 }}
    }},
    {{
      "name": "The Neutral Scenario",
      "narrative": "A descriptive story of a mixed economy...",
      "parameters": {{ "avg_equity_return": 9.0, "avg_bond_return": 6.5, "avg_inflation": 6.0 }}
    }}
  ]
}}
"""
forecaster_prompt = PromptTemplate.from_template(forecaster_template)

def project_goal_timeline(target_amount, initial_investment, monthly_contribution, annual_return_rate):
    if monthly_contribution <= 0 and initial_investment < target_amount:
        return float('inf')

    if annual_return_rate <= 0:
        if monthly_contribution <= 0:
            return float('inf')
        return (target_amount - initial_investment) / (monthly_contribution * 12)

    monthly_rate = (1 + annual_return_rate) ** (1/12) - 1
    
    if abs(monthly_rate) < 1e-9:
        if monthly_contribution <= 0:
            return float('inf')
        return (target_amount - initial_investment) / (monthly_contribution * 12)

    current_value = float(initial_investment)
    months = 0
    while current_value < target_amount:
        interest = current_value * monthly_rate
        current_value += interest + monthly_contribution
        months += 1
        if months > 1200:
            return float('inf')
            
    return round(months / 12, 1)

async def run_economic_forecaster(user_profile: dict):
    scenarios_str = await invoke_llm_with_retry(forecaster_prompt, {})
    
    start_index = scenarios_str.find('{')
    end_index = scenarios_str.rfind('}') + 1
    json_str = scenarios_str[start_index:end_index]
    scenarios_data = json.loads(json_str)

    monthly_savings = user_profile['monthly_income'] - user_profile['monthly_expenses'] - user_profile['liabilities']['loans_emi']
    initial_investment = user_profile['assets']['equity_investments'] + user_profile['assets']['other_investments']

    for scenario in scenarios_data['scenarios']:
        params = scenario['parameters']
        annual_return = params['avg_equity_return'] / 100

        projected_timelines = {}
        for goal in user_profile['goals']:
            timeline = project_goal_timeline(
                target_amount=float(goal['target_amount']),
                initial_investment=float(initial_investment),
                monthly_contribution=float(monthly_savings),
                annual_return_rate=float(annual_return)
            )
            projected_timelines[goal['name']] = "More than 100 years" if math.isinf(timeline) else f"{timeline} years"
        
        scenario['projected_timelines'] = projected_timelines
        
    return scenarios_data

# --- Agent 5: The Context-Aware Q&A Agent ---
qa_template = """
You are FinPilot, an expert and friendly financial advisor. A user is asking a follow-up question about the financial plan you have already created for them.
Your answer must be based ONLY on the context provided below. Be concise, helpful, and reassuring. Do not make up any information.

*CONTEXT - USER'S ORIGINAL PROFILE:*
{user_profile}

*CONTEXT - THE GENERATED PLAN:*
{generated_plan}

*CONTEXT - RECENT CHAT HISTORY:*
{chat_history}

Based on all of this context, answer the user's question.

*USER'S QUESTION:*
{new_question}

*YOUR ANSWER:*
"""
qa_prompt = PromptTemplate.from_template(qa_template)

async def run_qa_agent(payload: dict):
    qa_input = {
        "user_profile": json.dumps(payload['userProfile']),
        "generated_plan": json.dumps(payload['generatedPlan']),
        "chat_history": json.dumps(payload['chatHistory']),
        "new_question": payload['newQuestion']
    }
    answer = await invoke_llm_with_retry(qa_prompt, qa_input)
    return {"response": answer}