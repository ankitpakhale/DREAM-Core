from fastapi import FastAPI, Request, Response  # used in some other files
import uvicorn  # used in some other files
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any
from pydantic import BaseModel
import json
import os
from app.utils.constants import ROUTES
from app.services import dream_life_generation_service

# from app.utils import cache
from app.utils import logger, handle_response


# Create FastAPI app instance
app = FastAPI(
    title="DREAM",
    description="Dynamic Realization Engine for Achieving Milestones",
    version="1.0.0",
    openapi_version="1.0.0",
)

# Expose FastAPI framework components
App = app

# Configure CORS
App.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"
    ],  # specify origin for frontend like ["https://finddreamlife.com"]
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=[
        "Origin",
        "Content-Type",
        "Accept",
        "Authorization",
        "X-Is-Feedback-Loop",
        "X-Active-Client",
        "X-Is-Compare-Mode",
    ],
)


# Sample route to test server
@App.get("/")
def read_root():
    return {"message": "FastAPI CORS-configured app"}


# Sample route to test server
@App.get(ROUTES.HEALTHCHECK_ROUTE)
def ping():
    logger.debug("🐛 Ping() entry point hit")
    return {
        "payload": {},
        "message": "PONG",
        "status_code": 200,
    }


@App.get("/openapi.json")
def get_openapi():
    return JSONResponse(content=app.openapi())


# ################################## #
#   DREAM ENDPOINT CONFIGURATIONS    #
# ################################## #
def construct_sample_payload():
    parent_path = os.path.dirname(__file__).split("/")[:-2]
    relative_schema_path = ["app", "sample_data", "dream_life_response.json"]
    parent_path.extend(relative_schema_path)
    schema_path = "/".join(parent_path)

    with open(schema_path, "r", encoding="utf-8") as f:
        output_schema = json.load(f)

    return output_schema


# ——— Request model with every field you listed ———
class DreamPayload(BaseModel):
    career_fulfilling_career: str
    career_definition_of_success: str
    career_money_no_object: str
    career_irreplaceable_skills: str
    career_role_models: str
    career_work_environment: str
    career_work_team_individually: str
    career_ideal_work_life_balance: str
    career_work_from_anywhere: str
    career_impactful_project: str
    finance_financial_freedom: str
    finance_passive_income_needed: str
    finance_relationship_with_money: str
    finance_one_important_financial_decision: str
    finance_managing_spending: str
    finance_short_term_financial_goals: str
    finance_investment_choice: str
    finance_dream_budget: str
    finance_tracking_finances: str
    finance_impact_of_financial_freedom: str
    relationships_qualities_in_relationships: str
    relationships_prioritizing_relationships: str
    relationships_balancing_career_and_relationships: str
    relationships_ideal_partner_dynamic: str
    relationships_conflict_resolution: str
    relationships_legacy_in_relationships: str
    relationships_role_of_friendships: str
    relationships_contributing_to_others: str
    relationships_boundaries_for_healthy_relationships: str
    relationships_ideal_circle_of_people: str


# ——— Endpoint ———
# @cache
@handle_response
@App.post(ROUTES.DREAM_ROUTE)
async def dream(payload: DreamPayload) -> Dict[str, Any]:
    """
    Handle the dream based on JSON payload.
    """
    logger.debug("🤖 __generate_dream_life_handler route called")
    payload = payload.model_dump_json()
    logger.debug("🤖 Received payload: %s", payload)

    logger.debug("🤖 dream() entry point hit 1")
    # Start dream using the service
    _payload = json.loads(payload)
    response = await dream_life_generation_service.execute_task(payload=_payload)
    logger.debug("🤖 dream() entry point hit 2")

    return {
        "payload": response,
        "message": "Dream has been successfully completed!",
        "status_code": 200,
    }
