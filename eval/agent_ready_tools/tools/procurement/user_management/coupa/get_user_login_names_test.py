from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.user_management.coupa.get_user_login_names import (
    coupa_get_user_login_names,
)


def test_coupa_get_user_login_names() -> None:
    """Test that the `get_user_login_names` function returns the expected response."""
    # Define test data:
    test_data = {
        "user_login": "mjordan",
    }

    # Patch `get_coupa_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.user_management.coupa.get_user_login_names.get_coupa_client"
    ) as mock_coupa_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_coupa_client.return_value = mock_client
        mock_client.get_request.return_value = [
            {"login": test_data["user_login"]},
        ]

        # Get user Login names
        response = coupa_get_user_login_names()

        # Ensure that get_user_login_names() executed and returned proper values
        assert response
        assert len(response.login_names)
        assert response.login_names[0].login_name == test_data["user_login"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            resource_name="users",
            params={
                "status": "active",
                "limit": 10,
                "offset": 0,
            },
        )
