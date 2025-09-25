from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.salesforce.update_user import update_user


def test_update_user() -> None:
    """Tests that the `update_user` function returns the expected response."""

    # Define test data:
    test_data = {
        "user_id": "005gL000001aTanQAE",
        "first_name": "Integrations2",
        "last_name": "User12",
        "alias": "integ12",
        "country": "India",
        "company": "EPIC OrganizationFarm1",
    }

    test_response = 204

    # Patch `get_salesforce_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.salesforce.update_user.get_salesforce_client"
    ) as mock_salesforce_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_salesforce_client.return_value = mock_client
        mock_client.salesforce_object.User.update.return_value = test_response

        # Update User
        response = update_user(**test_data)

        # Ensure that update_user() has executed and returned proper values
        assert response
        assert response == test_response

        # Ensure the API call was made with expected parameters
        mock_client.salesforce_object.User.update(test_data, test_data["user_id"])
