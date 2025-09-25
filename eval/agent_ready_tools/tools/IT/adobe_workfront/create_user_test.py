from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.adobe_workfront.create_user import create_user


def test_create_user() -> None:
    """Verifies that the `create_user` tool can successfully create a user in Adobe Workfront."""

    # Define test data
    test_data = {
        "first_name": "Watson",
        "last_name": "Orchestrate",
        "email_address": "Orchestrate@gmail.com",
        "access_level_id": "66db21100646c6ae9dd4407ab4242935",
        "phone_number": "998812766655",
        "title": "Watson Agent",
        "my_info": "WatsonOrchestrate",
        "user_id": "68304ec800124e0cc977ae1873a70b0b",
        "name": "Watson Orchestrate",
    }

    # Patch `get_adobe_workfront_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.adobe_workfront.create_user.get_adobe_workfront_client"
    ) as mock_adobe_workfront_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_adobe_workfront_client.return_value = mock_client
        mock_client.post_request.return_value = {
            "data": {
                "ID": test_data["user_id"],
                "name": test_data["name"],
            }
        }
        # Create a user
        response = create_user(
            first_name=test_data["first_name"],
            last_name=test_data["last_name"],
            email_address=test_data["email_address"],
            access_level_id=test_data["access_level_id"],
            phone_number=test_data["phone_number"],
            title=test_data["title"],
            my_info=test_data["my_info"],
        )

        # Ensure that create_user() has executed and returned proper values
        assert response
        assert response.user_id == test_data["user_id"]
        assert response.name == test_data["name"]

        # Ensure the API call was made with expected parameters
        mock_client.post_request.assert_called_once_with(
            entity="user",
            payload={
                "lastName": test_data["last_name"],
                "firstName": test_data["first_name"],
                "emailAddr": test_data["email_address"],
                "accessLevelID": test_data["access_level_id"],
                "phoneNumber": test_data["phone_number"],
                "title": test_data["title"],
                "myInfo": test_data["my_info"],
            },
        )
