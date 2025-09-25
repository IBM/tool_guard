from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.adobe_workfront.delete_portfolio import delete_portfolio


def test_delete_portfolio() -> None:
    """Tests that a portfolio can be deleted successfully by the `delete_portfolio` tool."""
    # Define test data:
    test_data = {"portfolio_id": "682b16df0009b907a20c35a1b4dcc301", "http_code": 204}

    # Patch `get_adobe_workfront_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.adobe_workfront.delete_portfolio.get_adobe_workfront_client"
    ) as mock_adobe_workfront_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_adobe_workfront_client.return_value = mock_client
        mock_client.delete_request.return_value = test_data["http_code"]

        # Call the function
        response = delete_portfolio(portfolio_id=test_data["portfolio_id"])

        # Ensure that the delete_portfolio() has executed and returned the expected response
        assert response
        assert response.http_code == test_data["http_code"]

        # Ensure the API call was made with expected parameters
        mock_client.delete_request.assert_called_once_with(
            entity=f"port/{test_data["portfolio_id"]}"
        )
