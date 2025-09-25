from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.user_management.coupa.get_user_active_status import (
    coupa_get_user_active_status,
)


def test_coupa_get_user_active_status() -> None:
    """Test that the `get_user_active_status` function returns the expected response."""
    # Define test data:
    test_data = {
        "user_login": "emp0086",
    }

    # Patch `get_coupa_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.user_management.coupa.get_user_active_status.get_coupa_client"
    ) as mock_coupa_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_coupa_client.return_value = mock_client
        mock_client.get_request_list.return_value = [
            {"login": test_data["user_login"]},
        ]

        # Get user Login names
        response = coupa_get_user_active_status(login_name=test_data["user_login"])

        # Ensure that get_user_active_status() executed and returned proper values
        assert response
        assert response is True

        # Ensure the API call was made with expected parameters
        mock_client.get_request_list.assert_called_once_with(
            resource_name="users", params={"status": "active", "login": test_data["user_login"]}
        )
