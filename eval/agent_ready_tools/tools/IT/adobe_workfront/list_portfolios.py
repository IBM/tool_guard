from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.adobe_workfront_client import get_adobe_workfront_client
from agent_ready_tools.utils.tool_credentials import ADOBE_WORKFRONT_CONNECTIONS


@dataclass
class Portfolio:
    """Represents a portfolio in Adobe Workfront."""

    portfolio_id: str
    portfolio_name: str
    is_active: bool
    description: Optional[str]


@dataclass
class ListPortfolioResponse:
    """Represents the response for retrieving portfolios in Adobe Workfront."""

    portfolios: List[Portfolio]


@tool(expected_credentials=ADOBE_WORKFRONT_CONNECTIONS)
def list_portfolios(
    portfolio_name: Optional[str] = None,
    is_active: Optional[bool] = True,
    limit: Optional[int] = 100,
    skip: Optional[int] = 0,
) -> ListPortfolioResponse:
    """
    Gets a list of portfolios from Adobe Workfront.

    Args:
        portfolio_name: The name of the portfolio in Adobe Workfront.
        is_active: The status of the portfolio. If True, only active portfolios are retrieved. If
            False, only inactive porfolios are retrieved.
        limit: The maximum number of portfolios to return. Default is 100.
        skip: The number of portfolios to skip (for pagination). Default is 0.

    Returns:
        List of portfolios.
    """

    client = get_adobe_workfront_client()
    params = {"name": portfolio_name, "isActive": is_active, "$$LIMIT": limit, "$$FIRST": skip}

    params = {key: value for key, value in params.items() if value is not None}
    response = client.get_request(entity="port/search", params=params)

    portfolios: List[Portfolio] = [
        Portfolio(
            portfolio_id=result.get("ID", ""),
            portfolio_name=result.get("name", ""),
            is_active=result.get("isActive", True),
            description=result.get("description", ""),
        )
        for result in response.get("data", [])
    ]

    return ListPortfolioResponse(
        portfolios=portfolios,
    )
