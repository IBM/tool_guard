from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.adobe_workfront.create_portfolio import create_portfolio


def test_create_portfolio() -> None:
    """Verifies that the `create_portfolio` tool can successfully create a portfolio in Adobe
    Workfront."""

    # Define test data
    test_data = {
        "name": "Portfolio",
        "description": "Creating a portfolio",
        "owner_id": "67e168720af75981a4c50727a739cd29",
        "group_id": "62225baf0011b754d8df8eb624c0e1f6",
        "alignment_scorecard_id": "f8bb1e57154c423a9d9c5c9894d80607",
        "portfolio_id": "682b3a25000ac9d6e7196c10924a8cfc",
    }

    # Patch `get_adobe_workfront_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.adobe_workfront.create_portfolio.get_adobe_workfront_client"
    ) as mock_adobe_workfront_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_adobe_workfront_client.return_value = mock_client
        mock_client.post_request.return_value = {
            "data": {
                "ID": test_data["portfolio_id"],
                "name": test_data["name"],
            }
        }
        # Create a portfolio
        response = create_portfolio(
            name=test_data["name"],
            description=test_data["description"],
            owner_id=test_data["owner_id"],
            group_id=test_data["group_id"],
            alignment_scorecard_id=test_data["alignment_scorecard_id"],
        )

        # Ensure that create_portfolio() has executed and returned proper values
        assert response
        assert response.portfolio_id == test_data["portfolio_id"]
        assert response.name == test_data["name"]

        # Ensure the API call was made with expected parameters
        mock_client.post_request.assert_called_once_with(
            entity="port",
            payload={
                "name": test_data["name"],
                "description": test_data["description"],
                "ownerID": test_data["owner_id"],
                "groupID": test_data["group_id"],
                "alignmentScoreCardID": test_data["alignment_scorecard_id"],
            },
        )
