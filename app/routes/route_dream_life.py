from app.framework import App, Request
from app.services import dream_life_generation_service
from app.utils import logger, handle_response
from app.utils.constants import ROUTES
import os
import json


def construct_sample_payload():
    parent_path = os.path.dirname(__file__).split("/")[:-2]
    relative_schema_path = ["app", "sample_data", "dream_life_response.json"]
    parent_path.extend(relative_schema_path)
    schema_path = "/".join(parent_path)

    with open(schema_path, "r", encoding="utf-8") as f:
        output_schema = json.load(f)

    return output_schema


class DreamLifeRoute:
    """
    Singleton class to handle and register routes for dream.
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    @handle_response
    async def __generate_dream_life_handler(self, request: Request):
        """
        Handle the dream based on the payload.
        """
        logger.debug("__generate_dream_life_handler route called")

        # Parse the form data once
        form_data = await request.form()

        # Retrieve data from the parsed form data and make a dictionary object
        payload = {
            "career_fulfilling_career": form_data.get("career_fulfilling_career"),
            "career_definition_of_success": form_data.get(
                "career_definition_of_success"
            ),
            "career_money_no_object": form_data.get("career_money_no_object"),
            "career_irreplaceable_skills": form_data.get("career_irreplaceable_skills"),
            "career_role_models": form_data.get("career_role_models"),
            "career_work_environment": form_data.get("career_work_environment"),
            "career_work_team_individually": form_data.get(
                "career_work_team_individually"
            ),
            "career_ideal_work_life_balance": form_data.get(
                "career_ideal_work_life_balance"
            ),
            "career_work_from_anywhere": form_data.get("career_work_from_anywhere"),
            "career_impactful_project": form_data.get("career_impactful_project"),
            "finance_financial_freedom": form_data.get("finance_financial_freedom"),
            "finance_passive_income_needed": form_data.get(
                "finance_passive_income_needed"
            ),
            "finance_relationship_with_money": form_data.get(
                "finance_relationship_with_money"
            ),
            "finance_one_important_financial_decision": form_data.get(
                "finance_one_important_financial_decision"
            ),
            "finance_managing_spending": form_data.get("finance_managing_spending"),
            "finance_short_term_financial_goals": form_data.get(
                "finance_short_term_financial_goals"
            ),
            "finance_investment_choice": form_data.get("finance_investment_choice"),
            "finance_dream_budget": form_data.get("finance_dream_budget"),
            "finance_tracking_finances": form_data.get("finance_tracking_finances"),
            "finance_impact_of_financial_freedom": form_data.get(
                "finance_impact_of_financial_freedom"
            ),
            "relationships_qualities_in_relationships": form_data.get(
                "relationships_qualities_in_relationships"
            ),
            "relationships_prioritizing_relationships": form_data.get(
                "relationships_prioritizing_relationships"
            ),
            "relationships_balancing_career_and_relationships": form_data.get(
                "relationships_balancing_career_and_relationships"
            ),
            "relationships_ideal_partner_dynamic": form_data.get(
                "relationships_ideal_partner_dynamic"
            ),
            "relationships_conflict_resolution": form_data.get(
                "relationships_conflict_resolution"
            ),
            "relationships_legacy_in_relationships": form_data.get(
                "relationships_legacy_in_relationships"
            ),
            "relationships_role_of_friendships": form_data.get(
                "relationships_role_of_friendships"
            ),
            "relationships_contributing_to_others": form_data.get(
                "relationships_contributing_to_others"
            ),
            "relationships_boundaries_for_healthy_relationships": form_data.get(
                "relationships_boundaries_for_healthy_relationships"
            ),
            "relationships_ideal_circle_of_people": form_data.get(
                "relationships_ideal_circle_of_people"
            ),
        }
        logger.debug(f"Received payload: {payload}")

        # Start dream using the service
        # response = dream_life_generation_service.execute_task(payload=payload)
        response = construct_sample_payload()
        return {
            "payload": response,
            "message": "Dream has been successfully completed!",
            "status_code": 200,
        }

    def register(self):
        """
        Register the route for dream.
        """
        App.add_api_route(
            path=ROUTES.DREAM_ROUTE,
            endpoint=self.__generate_dream_life_handler,
            methods=["POST"],
        )


# Singleton instance of DreamLifeRoute
dream_life_route_obj = DreamLifeRoute()
