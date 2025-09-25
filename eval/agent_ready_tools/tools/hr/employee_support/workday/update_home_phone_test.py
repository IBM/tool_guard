from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.workday.update_home_phone import update_home_phone


def test_update_home_phone() -> None:
    """Test that the `update_home_phone` function returns the expected response."""

    # Define test data:
    test_data = {
        "user_id": "16d87047a76a47b399b4a677058d629f",
        "home_phone_id": "bc33aa3152ec42d4995f4791a106ed09",
        "new_home_phone": "+18729481658172",
        "effective_date": "2025-02-20",
        "status": "Successfully Completed",
        "description": "Home Contact Change: Chad Anderson",
        "change_id": "dc4945b8b8be429e87564e01889c69f5",
    }

    # Patch `get_workday_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.workday.update_home_phone.get_workday_client"
    ) as mock_workday_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_workday_client.return_value = mock_client
        mock_client.post_home_contact_information_changes.return_value = {
            "id": test_data["change_id"]
        }
        mock_client.update_home_phone.return_value = {
            "id": test_data["home_phone_id"],
            "completePhoneNumber": test_data["new_home_phone"],
        }
        mock_client.post_home_contact_information_changes_submit.return_value = {
            "businessProcessParameters": {"overallStatus": test_data["status"]},
            "descriptor": test_data["description"],
        }

        # Update the phone number
        response = update_home_phone(
            user_id=test_data["user_id"],
            effective_date=test_data["effective_date"],
            home_phone_id=test_data["home_phone_id"],
            new_home_phone=test_data["new_home_phone"],
        )

        # Ensure that update_home_email() executed and returned proper values
        assert response
        assert response.change_description == test_data["description"]
        assert response.request_status == test_data["status"]
        assert response.home_phone_id == test_data["home_phone_id"]
        assert response.new_home_phone == test_data["new_home_phone"]

        # Ensure the API calls was made with expected parameters
        mock_client.post_home_contact_information_changes.assert_called_once_with(
            user_id=test_data["user_id"], effective_date=test_data["effective_date"]
        )
        mock_client.update_home_phone.assert_called_once_with(
            home_contact_information_change_id=test_data["change_id"],
            home_phone_id=test_data["home_phone_id"],
            new_home_phone=test_data["new_home_phone"],
        )
        mock_client.post_home_contact_information_changes_submit.assert_called_once_with(
            home_contact_information_change_id=test_data["change_id"]
        )
