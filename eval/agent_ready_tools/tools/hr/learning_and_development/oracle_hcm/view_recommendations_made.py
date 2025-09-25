from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.oraclehcm_client import get_oracle_hcm_client
from agent_ready_tools.utils.tool_credentials import ORACLE_HCM_CONNECTIONS


@dataclass
class RecommendationDetailsResponse:
    """Represents the response from getting a worker's learning recommendations in Oracle HCM."""

    recommendations: List[str]


@tool(expected_credentials=ORACLE_HCM_CONNECTIONS)
def view_recommendations_made(
    person_id: int, limit: Optional[int] = 50
) -> RecommendationDetailsResponse:
    """
    Gets a worker's learning recommendations in Oracle HCM.

    Args:
        person_id: The person_id of the user, returned by the `get_user_oracle_ids` tool.
        limit: The maximum number of recommendations to retrieve in a single API call. Defaults to
            50. Use this to control the size of the result set.

    Returns:
        The learning recommendations made by the worker.
    """
    client = get_oracle_hcm_client()
    q_expr = f"assignerId={person_id}"
    params = {"limit": limit}
    response = client.get_request(
        "learningRecommendations",
        q_expr=q_expr,
        params=params,
        headers={"REST-Framework-Version": "4"},
    )

    # As there are duplicates in the learning recommendations, we have used this approach to filter out the duplicates
    # and retain only the unique learning recommendations
    recommendations = list(
        {
            recommendation: ""
            for recommendation in [result["learningItemTitle"] for result in response["items"]]
        }
    )

    return RecommendationDetailsResponse(recommendations=recommendations)
