from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.salesforce.update_account import update_account


def test_update_account() -> None:
    """Test that the `update_account` function returns the expected response."""

    # Define test data:
    test_data = {
        "account_id": "001gL000004Zin4QAC",
        "account_name": "Test-1 9th May - 2",
        "account_type": "Customer",
        "description": "Key account with high engagement",
        "number_of_employees": "1000",
        "annual_revenue": "2500000.0",
        "owner_id": "005gL000001qXQjQAM",
    }

    test_response = 204

    # Patch `get_salesforce_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.salesforce.update_account.get_salesforce_client"
    ) as mock_salesforce_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_salesforce_client.return_value = mock_client
        mock_client.salesforce_object.Account.update.return_value = test_response

        # Update account
        response = update_account(**test_data)

        # Ensure that update_account() executed and returned proper values
        assert response
        assert response == test_response

        # Ensure the API call was made with expected parameters
        mock_client.salesforce_object.Account.update(test_data["account_id"], test_data)
