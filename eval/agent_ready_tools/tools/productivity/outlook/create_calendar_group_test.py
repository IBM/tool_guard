from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.productivity.outlook.create_calendar_group import create_calendar_group


def test_create_calendar_group() -> None:
    """Verify that the `create_calendar_group` tool can successfully create a calendar group."""

    # Define test data:
    test_data = {
        "group_id": "123456789",
        "name": "Personal events 3",
        "status_code": 201,
        "user_name": "user@example.com",
    }

    # Patch `get_microsoft_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.productivity.outlook.create_calendar_group.get_microsoft_client"
    ) as mock_microsoft_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_microsoft_client.return_value = mock_client
        mock_client.post_request.return_value = {
            "id": test_data["group_id"],
            "status_code": test_data["status_code"],
        }
        mock_client.get_user_resource_path.return_value = f"users/{test_data["user_name"]}"

        # Create calendar group
        response = create_calendar_group(name=test_data["name"])

        # Ensure that create_calendar_group() executed and returned proper values
        assert response
        assert response.group_id == test_data["group_id"]
        assert response.http_code == test_data["status_code"]

        # Ensure the API call was made with expected parameters
        mock_client.post_request.assert_called_once_with(
            endpoint=f"users/{test_data["user_name"]}/calendarGroups",
            data={"name": test_data["name"]},
        )
