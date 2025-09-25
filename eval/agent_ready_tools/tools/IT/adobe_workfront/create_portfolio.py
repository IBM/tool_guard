from typing import Any, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.adobe_workfront_client import get_adobe_workfront_client
from agent_ready_tools.utils.tool_credentials import ADOBE_WORKFRONT_CONNECTIONS


@dataclass
class CreatePortfolioResponse:
    """Represents the result for portfolio creation in Adobe Workfront."""

    portfolio_id: str
    name: str


@tool(expected_credentials=ADOBE_WORKFRONT_CONNECTIONS)
def create_portfolio(
    name: str,
    description: Optional[str] = None,
    owner_id: Optional[str] = None,
    group_id: Optional[str] = None,
    alignment_scorecard_id: Optional[str] = None,
) -> CreatePortfolioResponse:
    """
    Creates a portfolio in Adobe Workfront.

    Args:
        name: The name of the portfolio.
        description: The description of the portfolio.
        owner_id: The id of the owner, returned by the `list_users` tool.
        group_id: The id of the group, returned by the `list_groups` tool.
        alignment_scorecard_id: The id of the alignment scorecard, returned by the `list_scorecards`
            tool.

    Returns:
        The result of creating a portfolio.
    """

    client = get_adobe_workfront_client()

    payload: dict[str, Any] = {
        "name": name,
        "description": description,
        "ownerID": owner_id,
        "groupID": group_id,
        "alignmentScoreCardID": alignment_scorecard_id,
    }
    payload = {key: value for key, value in payload.items() if value}

    response = client.post_request(entity="port", payload=payload)
    data = response.get("data", {})
    return CreatePortfolioResponse(portfolio_id=data.get("ID", ""), name=data.get("name", ""))
