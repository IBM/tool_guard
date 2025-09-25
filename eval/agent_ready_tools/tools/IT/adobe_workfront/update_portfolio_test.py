from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.adobe_workfront.update_portfolio import (
    UpdatePortfolioResponse,
    update_portfolio,
)


def test_update_portfolio() -> None:
    """Verifies that the `update_portfolio` tool updates the portfolio details in Adobe
    Workfront."""

    # Define test data:
    test_data = {
        "portfolio_id": "68306c10001399ae2347aeaddaf131c7",
        "portfolio_name": "Update a portfolio",
        "description": "Testing",
        "is_active": True,
        "owner_id": "67e168720af75981a4c50727a739cd29",
        "group_id": "62225baf0011b754d8df8eb624c0e1f6",
        "alignment_scorecard_id": "682c0e9100029f055125b9d4def4efff",
    }

    # Patch `get_adobe_workfront_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.adobe_workfront.update_portfolio.get_adobe_workfront_client"
    ) as mock_adobe_workfront_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_adobe_workfront_client.return_value = mock_client
        mock_client.put_request.return_value = {
            "data": {
                "name": test_data["portfolio_name"],
                "description": test_data["description"],
                "isActive": test_data["is_active"],
            }
        }

        # Update a portfolio
        response = update_portfolio(
            portfolio_id=test_data["portfolio_id"],
            portfolio_name=test_data["portfolio_name"],
            description=test_data["description"],
            is_active=test_data["is_active"],
            owner_id=test_data["owner_id"],
            group_id=test_data["group_id"],
            alignment_scorecard_id=test_data["alignment_scorecard_id"],
        )

        expected_response = UpdatePortfolioResponse(
            portfolio_name=str(test_data["portfolio_name"]),
            description=str(test_data["description"]),
            is_active=bool(test_data["is_active"]),
        )

        # Ensure that update_portfolio() executed and returned proper values
        assert response
        assert response == expected_response

        # Ensure the API call was made with expected parameters
        mock_client.put_request.assert_called_once_with(
            entity=f"port/{test_data['portfolio_id']}",
            payload={
                "name": test_data["portfolio_name"],
                "description": test_data["description"],
                "isActive": test_data["is_active"],
                "ownerID": test_data["owner_id"],
                "groupID": test_data["group_id"],
                "alignmentScoreCardID": test_data["alignment_scorecard_id"],
            },
        )
