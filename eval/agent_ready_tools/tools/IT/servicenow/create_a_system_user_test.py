from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.servicenow.create_a_system_user import create_a_system_user


def test_create_a_system_user() -> None:
    """Test that a system user can be created successfully by the `create_a_system_user` tool."""

    # Define test data:
    test_data = {
        "user_name": "systemsaisharan",
        "email": "sysuser@gmail.com",
        "first_name": "sys",
        "last_name": "user",
        "gender": "male",
        "mobile_phone": "1234567890",
        "title": "system",
        "user_password": "password",
        "http_code": 201,
    }

    # Patch `get_servicenow_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.servicenow.create_a_system_user.get_servicenow_client"
    ) as mock_servicenow_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_servicenow_client.return_value = mock_client
        mock_client.post_request.return_value = {
            "result": {"user_name": test_data["user_name"], "email": test_data["email"]},
            "status_code": test_data["http_code"],
        }

        # Create a system user
        response = create_a_system_user(
            user_name=test_data["user_name"],
            email=test_data["email"],
            first_name=test_data["first_name"],
            last_name=test_data["last_name"],
            gender=test_data["gender"],
            mobile_phone=test_data["mobile_phone"],
            title=test_data["title"],
            user_password=test_data["user_password"],
        )

        # Ensure that create_a_system_user() executed and returned proper values
        assert response
        assert response.http_code == test_data["http_code"]
        assert response.user_name == test_data["user_name"]
        assert response.email == test_data["email"]

        # Ensure the API call was made with expected parameters
        mock_client.post_request.assert_called_once_with(
            entity="sys_user",
            payload={
                "user_name": test_data["user_name"],
                "first_name": test_data["first_name"],
                "last_name": test_data["last_name"],
                "gender": test_data["gender"],
                "email": test_data["email"],
                "mobile_phone": test_data["mobile_phone"],
                "title": test_data["title"],
                "user_password": test_data["user_password"],
            },
        )
