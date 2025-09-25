from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.workday.update_home_email import update_home_email


def test_update_home_email() -> None:
    """Test that the `update_home_email` function returns the expected response."""

    # Define test data:
    test_data = {
        "user_id": "ca392111583a102b55041fd6ebc85b93",
        "email_id": "bc33aa3152ec42d4995f4791a106ed09",
        "new_email": "test.wxo@workday.com",
        "effective_date": "2025-02-20",
        "status": "Successfully Completed",
        "description": "Home Contact Change: Adrian Martin (On Leave)",
        "change_id": "dc4945b8b8be429e87564e01889c69f5",
    }

    # Patch `get_workday_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.workday.update_home_email.get_workday_client"
    ) as mock_workday_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_workday_client.return_value = mock_client
        mock_client.post_home_contact_information_changes.return_value = {
            "id": test_data["change_id"]
        }
        mock_client.update_home_email.return_value = {
            "id": test_data["email_id"],
            "emailAddress": test_data["new_email"],
        }
        mock_client.post_home_contact_information_changes_submit.return_value = {
            "businessProcessParameters": {"overallStatus": test_data["status"]},
            "descriptor": test_data["description"],
        }

        # Update the home email
        response = update_home_email(
            user_id=test_data["user_id"],
            effective_date=test_data["effective_date"],
            home_email_id=test_data["email_id"],
            new_home_email=test_data["new_email"],
        )

        # Ensure that update_home_email() executed and returned proper values
        assert response
        assert response.change_description == test_data["description"]
        assert response.request_status == test_data["status"]
        assert response.email_id == test_data["email_id"]
        assert response.new_email_address == test_data["new_email"]

        # Ensure the API calls was made with expected parameters
        mock_client.post_home_contact_information_changes.assert_called_once_with(
            user_id=test_data["user_id"], effective_date=test_data["effective_date"]
        )
        mock_client.update_home_email.assert_called_once_with(
            home_contact_information_change_id=test_data["change_id"],
            home_email_id=test_data["email_id"],
            new_home_email=test_data["new_email"],
        )
        mock_client.post_home_contact_information_changes_submit.assert_called_once_with(
            home_contact_information_change_id=test_data["change_id"]
        )


def test_add_home_email() -> None:
    """Test that the `update_home_email` function returns the expected response."""

    # Define test data:
    test_data = {
        "user_id": "ca392111583a102b55041fd6ebc85b93",
        "email_id": "bc33aa3152ec42d4995f4791a106ed09",
        "new_email": "test1.wxo@workday.com",
        "effective_date": "2025-02-20",
        "status": "Successfully Completed",
        "description": "Home Contact Change: Adrian Martin (On Leave)",
        "change_id": "dc4945b8b8be429e87564e01889c69f5",
    }

    # Patch `get_workday_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.workday.update_home_email.get_workday_client"
    ) as mock_workday_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_workday_client.return_value = mock_client
        mock_client.post_home_contact_information_changes.return_value = {
            "id": test_data["change_id"]
        }
        mock_client.add_home_email.return_value = {
            "id": test_data["email_id"],
            "emailAddress": test_data["new_email"],
        }
        mock_client.post_home_contact_information_changes_submit.return_value = {
            "businessProcessParameters": {"overallStatus": test_data["status"]},
            "descriptor": test_data["description"],
        }

        # Update the home email
        response = update_home_email(
            user_id=test_data["user_id"],
            effective_date=test_data["effective_date"],
            home_email_id="NULL",
            new_home_email=test_data["new_email"],
        )

        # Ensure that update_home_email() executed and returned proper values
        assert response
        assert response.change_description == test_data["description"]
        assert response.request_status == test_data["status"]
        assert response.new_email_address == test_data["new_email"]

        # Ensure the API calls was made with expected parameters
        mock_client.post_home_contact_information_changes.assert_called_once_with(
            user_id=test_data["user_id"], effective_date=test_data["effective_date"]
        )
        mock_client.add_home_email.assert_called_once_with(
            home_contact_information_change_id=test_data["change_id"],
            new_home_email=test_data["new_email"],
        )
        mock_client.post_home_contact_information_changes_submit.assert_called_once_with(
            home_contact_information_change_id=test_data["change_id"]
        )
