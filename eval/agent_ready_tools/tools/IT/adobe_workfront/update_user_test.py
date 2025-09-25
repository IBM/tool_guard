from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.adobe_workfront.update_user import (
    UpdateUserResponse,
    adobe_update_user,
)


def test_adobe_update_user() -> None:
    """Verifies that the `adobe_update_user` tool updates the user details in Adobe Workfront."""

    # Define test data:
    test_data = {
        "user_id": "68300719000b4ff6b5505e1beb6bee65",
        "first_name": "Kishore",
        "last_name": "Babu",
        "title": "Developer",
        "my_info": "Software developer at Wipro",
        "phone_number": "9199145456",
        "work_hours_per_day": 9.5,
        "address": "Gachibowli",
        "postal_code": "500031",
        "city_name": "Hyderabad",
        "state_name": "Telangana",
        "country_name": "India",
    }

    # Patch `get_adobe_workfront_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.adobe_workfront.update_user.get_adobe_workfront_client"
    ) as mock_adobe_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_adobe_client.return_value = mock_client
        mock_client.put_request.return_value = {
            "data": {
                "ID": test_data["user_id"],
                "title": test_data["title"],
                "myInfo": test_data["my_info"],
            }
        }

        # Update a user
        response = adobe_update_user(
            user_id=test_data["user_id"],
            first_name=test_data["first_name"],
            last_name=test_data["last_name"],
            title=test_data["title"],
            my_info=test_data["my_info"],
            phone_number=test_data["phone_number"],
            work_hours_per_day=test_data["work_hours_per_day"],
            address=test_data["address"],
            postal_code=test_data["postal_code"],
            city_name=test_data["city_name"],
            state_name=test_data["state_name"],
            country_name=test_data["country_name"],
        )

        expected_response = UpdateUserResponse(
            user_id=str(test_data["user_id"]),
            title=str(test_data["title"]),
            my_info=str(test_data["my_info"]),
        )

        # Ensure that adobe_update_user() executed and returned proper values
        assert response
        assert response == expected_response

        # Ensure the API call was made with expected parameters
        mock_client.put_request.assert_called_once_with(
            entity=f"user/{test_data['user_id']}",
            payload={
                "firstName": test_data["first_name"],
                "lastName": test_data["last_name"],
                "title": test_data["title"],
                "myInfo": test_data["my_info"],
                "phoneNumber": test_data["phone_number"],
                "workHoursPerDay": test_data["work_hours_per_day"],
                "address": test_data["address"],
                "postalCode": test_data["postal_code"],
                "city": test_data["city_name"],
                "state": test_data["state_name"],
                "country": test_data["country_name"],
            },
        )
