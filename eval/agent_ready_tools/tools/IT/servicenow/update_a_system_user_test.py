from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.servicenow.update_a_system_user import update_a_system_user


def test_update_a_system_user() -> None:
    """Test that the system user can be updated successfully by the `update_a_system_user` tool."""

    # Define test data:
    test_data = {
        "user_name_system_id": "03cfd3ac831c2e10e73115a6feaad355",
        "email": "abctest@example.com",
        "user_password": "1Password*",
        "phone": "1234567799",
        "title": "Test engineer",
        "department_system_id": "Financial operations",
        "country": "Financial operations",
        "http_code": 200,
    }

    # Patch `get_servicenow_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.servicenow.update_a_system_user.get_servicenow_client"
    ) as mock_servicenow_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_servicenow_client.return_value = mock_client
        mock_client.patch_request.return_value = {"status_code": test_data["http_code"]}

        # Update a system user
        response = update_a_system_user(
            user_name_system_id=test_data["user_name_system_id"],
            email=test_data["email"],
            user_password=test_data["user_password"],
            phone=test_data["phone"],
            title=test_data["title"],
            department_system_id=test_data["department_system_id"],
            country=test_data["country"],
        )

        # Ensure that update_a_system_user() executed and returned proper values
        assert response
        assert response.http_code == 200

        # Ensure the API call was made with expected parameters
        mock_client.patch_request.assert_called_once_with(
            entity="sys_user",
            entity_id=test_data["user_name_system_id"],
            payload={
                "email": test_data["email"],
                "user_password": test_data["user_password"],
                "phone": test_data["phone"],
                "title": test_data["title"],
                "department": test_data["department_system_id"],
                "country": test_data["country"],
            },
        )
