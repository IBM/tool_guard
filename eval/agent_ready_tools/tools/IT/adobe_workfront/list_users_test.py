from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.adobe_workfront.list_users import (
    AdobeUser,
    ListUsersResponse,
    adobe_list_users,
)


def test_adobe_list_users() -> None:
    """Verify that the `adobe_list_users` tool can successfully retrieve Adobe workfront users."""

    # Define test data:
    test_data = {
        "user_id": "6629314904c37a5dd4dd3cf79b5d5285",
        "user_name": "Aaron Albertson",
        "title": None,
        "email": "albertaa@us.ibm.com",
        "phone_number": None,
        "access_level": {
            "access_level_id": "66019d41001c09117fec70c3418359f0",
            "access_level_name": "QMX Document Owner",
        },
    }
    limit = 50
    fields = "title,emailAddr,phoneNumber,accessLevel"

    # Patch `get_adobe_workfront_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.adobe_workfront.list_users.get_adobe_workfront_client"
    ) as mock_get_adobe_workfront_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_get_adobe_workfront_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "data": [
                {
                    "ID": test_data["user_id"],
                    "name": test_data["user_name"],
                    "title": test_data["title"],
                    "emailAddr": test_data["email"],
                    "phoneNumber": test_data["phone_number"],
                    "accessLevel": (
                        {
                            "ID": test_data["access_level"]["access_level_id"],
                            "name": test_data["access_level"]["access_level_name"],
                        }
                        if isinstance(test_data["access_level"], dict)
                        else None
                    ),
                }
            ]
        }

        # Get adobe workfront users
        response = adobe_list_users(user_name=test_data["user_name"], email=test_data["email"])

        # Ensure title and phone_number are strings or None
        title = test_data["title"]
        if isinstance(title, dict):
            title = title.get("value", None)

        phone_number = test_data["phone_number"]
        if isinstance(phone_number, dict):
            phone_number = phone_number.get("value", None)

        # Ensure that adobe_list_users() executed and returned proper values
        expected_data = ListUsersResponse(
            users=[
                AdobeUser(
                    user_id=str(test_data["user_id"]),
                    user_name=str(test_data["user_name"]),
                    title=title,
                    email=str(test_data["email"]),
                    phone_number=phone_number,
                    access_level_id=(
                        str(test_data["access_level"]["access_level_id"])
                        if isinstance(test_data["access_level"], dict)
                        else None
                    ),
                    access_level_name=(
                        str(test_data["access_level"]["access_level_name"])
                        if isinstance(test_data["access_level"], dict)
                        else None
                    ),
                )
            ]
        )

        assert response == expected_data

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            entity="user/search",
            params={
                "name": test_data["user_name"],
                "emailAddr": test_data["email"],
                "fields": fields,
                "$$LIMIT": limit,
            },
        )
