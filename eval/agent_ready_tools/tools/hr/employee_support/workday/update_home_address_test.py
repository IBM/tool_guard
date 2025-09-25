from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.workday.update_home_address import (
    update_home_address,
)


def test_update_home_address() -> None:
    """Test that the `update_home_address` function returns the expected response."""

    # Define test data:
    test_data = {
        "user_id": "ca392111583a102b55041fd6ebc85b93",
        "effective_date": "2025-03-10",
        "address_line_1": "1750 Woodrose Ave",
        "address_line_2": "Apt 1234",
        "city": "Los Angeles",
        "postal_code": "95241",
        "is_primary": True,
        "country_id": "bc33aa3152ec42d4995f4791a106ed09",
        "state_id": "ec3d210e4240442e99a28fa70419aec5",
        "address_id": "d3fd6c7cdbf1101b037a564a1aba0c28",
        "change_id": "dc4945b8b8be429e87564e01889c69f5",
    }

    # Patch `get_workday_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.workday.update_home_address.get_workday_client"
    ) as mock_workday_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_workday_client.return_value = mock_client
        mock_client.post_home_contact_information_changes.return_value = {
            "id": test_data["change_id"]
        }
        mock_client.put_home_address.return_value = {
            "id": test_data["address_id"],
            "addressLine1": test_data["address_line_1"],
            "city": test_data["city"],
            "countryRegion": {"id": test_data["state_id"]},
            "country": {"id": test_data["country_id"]},
            "postalCode": test_data["postal_code"],
        }
        mock_client.post_home_contact_information_changes_submit.return_value = {
            "businessProcessParameters": {"overallStatus": "Successfully Completed"}
        }

        # Update home address
        response = update_home_address(
            user_id=test_data["user_id"],
            address_id=test_data["address_id"],
            effective_date=test_data["effective_date"],
            address_line_1=test_data["address_line_1"],
            address_line_2=test_data["address_line_2"],
            city=test_data["city"],
            state_id=test_data["state_id"],
            country_id=test_data["country_id"],
            postal_code=test_data["postal_code"],
            is_primary=test_data["is_primary"],
        )

        # Ensure that update_home_address() executed and returned proper values
        assert response
        assert response.address_id == test_data["address_id"]
        assert response.address_line_1 == test_data["address_line_1"]
        assert response.city == test_data["city"]
        assert response.state_id == test_data["state_id"]
        assert response.country_id == test_data["country_id"]
        assert response.postal_code == test_data["postal_code"]

        # Ensure the API calls was made with expected parameters
        mock_client.post_home_contact_information_changes.assert_called_once_with(
            user_id=test_data["user_id"], effective_date=test_data["effective_date"]
        )
        mock_client.put_home_address.assert_called_once_with(
            home_contact_information_changes_id=test_data["change_id"],
            address_id=test_data["address_id"],
            address_line_1=test_data["address_line_1"],
            address_line_2=test_data["address_line_2"],
            city=test_data["city"],
            state_id=test_data["state_id"],
            country_id=test_data["country_id"],
            postal_code=test_data["postal_code"],
            is_primary=test_data["is_primary"],
        )
        mock_client.post_home_contact_information_changes_submit.assert_called_once_with(
            home_contact_information_change_id=test_data["change_id"]
        )
