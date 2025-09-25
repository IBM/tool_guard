from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.servicenow.get_system_users import get_system_users


def test_get_system_users() -> None:
    """Test that the `get_system_users` function returns the expected response."""

    # Define test data:
    test_data = {
        "user_name": "sysadm",
        "name": "system user",
        "id": "b97e89b94a36231201676b73322a0311",
        "title": "system admin",
        "email": "sysadmin@gmail.com",
        "phone": "0987654321",
        "gender": "Male",
        "cost_center": "Customer Support",
        "manager": "Billie Cowley",
        "company": "ACME North America",
        "department": "Development",
        "limit": 10,
        "skip": 0,
    }

    # Patch `get_servicenow_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.servicenow.get_system_users.get_servicenow_client"
    ) as mock_servicenow_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_servicenow_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "result": [
                {
                    "user_name": test_data["user_name"],
                    "name": test_data["name"],
                    "sys_id": test_data["id"],
                    "title": test_data["title"],
                    "phone": test_data["phone"],
                    "email": test_data["email"],
                    "gender": "Male",
                    "cost_center": test_data["cost_center"],
                    "manager": test_data["manager"],
                    "company": test_data["company"],
                    "department": test_data["department"],
                },
            ],
        }

        # Get system users
        response = get_system_users(user_name=test_data["user_name"])

        # Ensure that get_system_users() executed and returned proper values
        assert response
        assert len(response.system_users)
        assert response.system_users[0].system_id == test_data["id"]
        assert response.system_users[0].user_name == test_data["user_name"]
        assert response.system_users[0].name == test_data["name"]
        assert response.system_users[0].email == test_data["email"]
        assert response.system_users[0].phone == test_data["phone"]
        assert response.system_users[0].cost_center == test_data["cost_center"]
        assert response.system_users[0].manager == test_data["manager"]
        assert response.system_users[0].company == test_data["company"]
        assert response.system_users[0].department == test_data["department"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            entity="sys_user",
            params={
                "user_name": test_data["user_name"],
                "sysparm_limit": test_data["limit"],
                "sysparm_offset": test_data["skip"],
                "sysparm_display_value": True,
            },
        )
