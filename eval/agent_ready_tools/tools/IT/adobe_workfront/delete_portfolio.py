from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.adobe_workfront_client import get_adobe_workfront_client
from agent_ready_tools.utils.tool_credentials import ADOBE_WORKFRONT_CONNECTIONS


@dataclass
class DeletePortfolioResponse:
    """Represents the result of delete operation performed on a portfolio in Adobe Workfront."""

    http_code: int


@tool(expected_credentials=ADOBE_WORKFRONT_CONNECTIONS)
def delete_portfolio(portfolio_id: str) -> DeletePortfolioResponse:
    """
    Deletes a portfolio in Adobe Workfront.

    Args:
        portfolio_id: The id of the portfolio, returned by the `list_portfolios` tool.

    Returns:
        The status of the delete operation.
    """

    client = get_adobe_workfront_client()

    response = client.delete_request(entity=f"port/{portfolio_id}")
    return DeletePortfolioResponse(http_code=response)
