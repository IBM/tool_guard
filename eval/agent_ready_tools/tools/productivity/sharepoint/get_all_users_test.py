from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.productivity.sharepoint.get_all_users import get_all_users


def test_get_all_users() -> None:
    """Verify that the `get_all_users` tool can successfully retrieve Microsoft users."""

    # Define test data:
    test_data = {
        "users": [
            {
                "id": "user-id-1",
                "displayName": "John Doe",
                "jobTitle": "Software Engineer",
                "mail": "john.doe@example.com",
            },
            {
                "id": "user-id-2",
                "displayName": "Jane Smith",
                "jobTitle": "Product Manager",
                "mail": "jane.smith@example.com",
            },
        ]
    }

    # Patch `get_microsoft_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.productivity.sharepoint.get_all_users.get_microsoft_client"
    ) as mock_microsoft_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_microsoft_client.return_value = mock_client
        mock_client.get_request.return_value = {"value": test_data["users"]}

        # Get Sharepoint users
        response = get_all_users()

        # Ensure that get_all_users() executed and returned proper values
        assert response
        assert len(response.users) == 2
        assert response.users[0].id == test_data["users"][0]["id"]
        assert response.users[0].display_name == test_data["users"][0]["displayName"]
        assert response.users[1].id == test_data["users"][1]["id"]
        assert response.users[1].display_name == test_data["users"][1]["displayName"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            "users?$select=id,displayName,jobTitle,mail"
        )
