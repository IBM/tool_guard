from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.sap_successfactors.sap_utility import user_exists


def test_user_exists_called_once() -> None:
    """Tests that the `user_exists` function returns the expected response."""
    # Define test data:
    test_data = {"user_id": "Tchin"}

    # Patch `get_sap_successfactors_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.sap_successfactors.sap_utility.get_sap_successfactors_client"
    ) as mock_get_client:

        # Create a mock client instance
        mock_client = MagicMock()
        mock_response = {"d": {"results": [{"userId": test_data["user_id"]}]}}

        mock_client.get_request.return_value = mock_response
        mock_get_client.return_value = mock_client

        # Check user exists
        result = user_exists(test_data["user_id"])

        # Ensure that user_exists() executed and returned proper values
        assert result

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            entity="User", filter_expr=f"userId eq '{test_data['user_id']}'"
        )
