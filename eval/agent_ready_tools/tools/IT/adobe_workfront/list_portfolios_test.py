from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.adobe_workfront.list_portfolios import (
    ListPortfolioResponse,
    Portfolio,
    list_portfolios,
)


def test_list_portfolios() -> None:
    """Verify that the `list_portfolios` tool can successfully retrieves all the portfolios in Adobe
    Workfront."""

    # Define test data:
    test_data = {
        "portfolio_id": "66d9a035000ee7c1c89bbcfbe1f74f61",
        "portfolio_name": "Distributech Tech 2025",
        "is_active": True,
        "description": "null",
    }
    limit = 100
    skip = 0

    # Patch `get_adobe_workfront_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.adobe_workfront.list_portfolios.get_adobe_workfront_client"
    ) as mock_get_adobe_workfront_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_get_adobe_workfront_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "data": [
                {
                    "ID": test_data["portfolio_id"],
                    "name": test_data["portfolio_name"],
                    "isActive": test_data["is_active"],
                    "description": test_data["description"],
                }
            ]
        }

        # Get adobe_workfront portfolios
        response = list_portfolios(portfolio_name=test_data["portfolio_name"])

        # Ensure that list_portfolios() executed and returned proper values

        expected_data = ListPortfolioResponse(
            portfolios=[
                Portfolio(
                    portfolio_id=str(test_data["portfolio_id"]),
                    portfolio_name=str(test_data["portfolio_name"]),
                    is_active=bool(test_data["is_active"]),
                    description=str(test_data["description"]),
                )
            ]
        )

        assert response == expected_data

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            entity="port/search",
            params={
                "name": test_data["portfolio_name"],
                "isActive": True,
                "$$LIMIT": limit,
                "$$FIRST": skip,
            },
        )
