from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.workday.get_home_email import get_home_email


def test_get_home_email() -> None:
    """Test that the `get_home_email` function returns the expected response."""

    # Define test data:
    test_data = {
        "person_id": "dc4945b8b8be429e87564e01889c69f5",
        "email_id": "d3fd6c7cdbf1101b037a564a1aba0c28",
        "email_address": "test.email@example.com",
    }

    # Patch `get_workday_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.workday.get_home_email.get_workday_client"
    ) as mock_workday_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_workday_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "data": [
                {
                    "id": test_data["email_id"],
                    "emailAddress": test_data["email_address"],
                }
            ],
        }

        # Get home email
        response = get_home_email(person_id=test_data["person_id"])

        # Ensure that get_home_email() executed and returned proper values
        assert response
        assert len(response.email_addresses)
        assert response.email_addresses[0].email_address == test_data["email_address"]
        assert response.email_addresses[0].email_id == test_data["email_id"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            url=f"api/person/v4/{mock_client.tenant_name}/people/{test_data['person_id']}/homeEmails"
        )
