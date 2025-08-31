import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
# CORRECTED: Typo fixed from 'pantic' to 'pydantic'
from pydantic import BaseModel, Field
from typing import List, Dict
from services.langchain_service import (
    generate_plan_with_assembly_line,
    run_economic_forecaster,
    run_qa_agent
)

# --- Pydantic Models (Data Contracts) ---
class Asset(BaseModel):
    cash_equivalents: float = Field(..., ge=0)
    equity_investments: float = Field(..., ge=0)
    other_investments: float = Field(0, ge=0)

class Liability(BaseModel):
    high_interest_debt: float = Field(..., ge=0)
    loans_emi: float = Field(..., ge=0)

class Goal(BaseModel):
    name: str = Field(..., min_length=1)
    target_amount: float = Field(..., gt=0)
    timeline_years: int = Field(..., gt=0)

class UserProfile(BaseModel):
    name: str
    age: int = Field(..., gt=0, lt=100)
    monthly_income: float = Field(..., ge=0)
    monthly_expenses: float = Field(..., ge=0)
    assets: Asset
    liabilities: Liability
    goals: List[Goal]
    risk_profile_answers: List[int]

class SimulationPayload(BaseModel):
    userProfile: UserProfile

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatPayload(BaseModel):
    userProfile: UserProfile
    generatedPlan: Dict
    chatHistory: List[ChatMessage]
    newQuestion: str

# --- FastAPI Application Setup ---
app = FastAPI(
    title="FinPilot API",
    description="The AI-powered backend for FinPilot, featuring a multi-agent financial planning system."
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- API Endpoints ---
@app.get("/", tags=["Root"])
async def read_root():
    return {"status": "FinPilot API is running!"}

@app.post("/generate-plan", tags=["Planning"])
async def generate_plan_endpoint(user_profile: UserProfile):
    print("Received profile, triggering AI Assembly Line...")
    try:
        plan_str = await generate_plan_with_assembly_line(user_profile.dict())
        start_index = plan_str.find('{')
        end_index = plan_str.rfind('}') + 1
        if start_index == -1 or end_index == 0:
            raise ValueError("No JSON object found in the AI's response.")
        json_str = plan_str[start_index:end_index]
        plan_json = json.loads(json_str)
        print("Successfully generated and parsed plan.")
        return plan_json
    except (json.JSONDecodeError, ValueError) as e:
        print(f"Error parsing JSON from AI response: {e}\nRaw AI Output was:\n---\n{plan_str}\n---")
        raise HTTPException(status_code=500, detail="AI returned an invalid JSON format.")
    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred while generating the plan: {e}")

@app.post("/simulate-scenarios", tags=["Simulation"])
async def simulate_scenarios_endpoint(payload: SimulationPayload):
    print("Received request for /simulate-scenarios")
    try:
        scenarios = await run_economic_forecaster(payload.userProfile.dict())
        return scenarios
    except Exception as e:
        print(f"An error occurred during simulation: {e}")
        raise HTTPException(status_code=500, detail="Failed to run simulation.")

@app.post("/chat", tags=["Q&A"])
async def chat_with_plan_endpoint(payload: ChatPayload):
    print("Received request for /chat")
    try:
        response = await run_qa_agent(payload.dict())
        return response
    except Exception as e:
        print(f"An error occurred during chat: {e}")
        raise HTTPException(status_code=500, detail="Failed to get chat response.")