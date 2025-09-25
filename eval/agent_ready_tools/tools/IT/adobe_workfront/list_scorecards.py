from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.adobe_workfront_client import get_adobe_workfront_client
from agent_ready_tools.utils.tool_credentials import ADOBE_WORKFRONT_CONNECTIONS


@dataclass
class Scorecard:
    """Represents a single scorecard in Adobe Workfront."""

    scorecard_id: str
    scorecard_name: str
    description: Optional[str]


@dataclass
class ListScorecardsResponse:
    """Represents the response for retrieving scorecards in Adobe Workfront."""

    scorecards: List[Scorecard]


@tool(expected_credentials=ADOBE_WORKFRONT_CONNECTIONS)
def list_scorecards(
    scorecard_name: Optional[str] = None,
    limit: Optional[int] = 50,
    skip: Optional[int] = 0,
) -> ListScorecardsResponse:
    """
    Gets a list of scorecards from Adobe Workfront.

    Args:
        scorecard_name: The name of the scorecard in Adobe Workfront.
        limit: The maximum number of scorecards to retrieve in a single API call. Defaults to 50.
            Use this to control the size of the result set.
        skip: The number of scorecards to skip for pagination purposes. Use this to retrieve
            subsequent pages of results when handling large datasets.

    Returns:
        List of scorecards.
    """

    client = get_adobe_workfront_client()

    params = {"name": scorecard_name, "$$LIMIT": limit, "$$FIRST": skip}

    # Filters out the parameter that are None.
    params = {key: value for key, value in params.items() if value is not None}

    response = client.get_request(entity="score/search", params=params)

    scorecards: List[Scorecard] = [
        Scorecard(
            scorecard_id=result.get("ID", ""),
            scorecard_name=result.get("name", ""),
            description=result.get("description", ""),
        )
        for result in response.get("data", [])
    ]

    return ListScorecardsResponse(
        scorecards=scorecards,
    )
