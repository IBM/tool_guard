from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import ToolPermission, tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.adobe_workfront_client import get_adobe_workfront_client
from agent_ready_tools.utils.tool_credentials import ADOBE_WORKFRONT_CONNECTIONS


@dataclass
class UpdatePortfolioResponse:
    """Represents the response for updating a portfolio in Adobe Workfront."""

    portfolio_name: str
    is_active: bool
    description: Optional[str]


@tool(
    permission=ToolPermission.WRITE_ONLY,
    expected_credentials=ADOBE_WORKFRONT_CONNECTIONS,
)
def update_portfolio(
    portfolio_id: str,
    portfolio_name: Optional[str] = None,
    description: Optional[str] = None,
    owner_id: Optional[str] = None,
    group_id: Optional[str] = None,
    alignment_scorecard_id: Optional[str] = None,
    is_active: Optional[bool] = True,
) -> UpdatePortfolioResponse:
    """
    Updates a portfolio in Adobe Workfront.

    Args:
        portfolio_id: The id of the portfolio, returned by the `list_portfolios` tool.
        portfolio_name: The name of the portfolio.
        description: The description of the portfolio.
        owner_id: The id of the owner, returned by the `list_users` tool.
        group_id: The id of the group, returned by the `list_groups` tool.
        alignment_scorecard_id: The id of the alignment scorecard, returned by the `list_scorecards`
            tool.
        is_active: The status of the portfolio in Adobe Workfront.

    Returns:
        The result of performing an update operation on a portfolio.
    """

    client = get_adobe_workfront_client()

    payload = {
        "name": portfolio_name,
        "description": description,
        "isActive": is_active,
        "ownerID": owner_id,
        "groupID": group_id,
        "alignmentScoreCardID": alignment_scorecard_id,
    }
    payload = {key: value for key, value in payload.items() if value}

    response = client.put_request(entity=f"port/{portfolio_id}", payload=payload)

    data = response.get("data", {})

    return UpdatePortfolioResponse(
        portfolio_name=data.get("name", ""),
        description=data.get("description", ""),
        is_active=data.get("isActive"),
    )
