from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.workday.get_home_phones import get_home_phones


def test_get_home_phones() -> None:
    """Test that the `get_home_phones` function returns the expected response."""

    # Define test data:
    test_data = {
        "person_id": "edde84f38de1494b9c7911dcc5c40bc6",
        "phone_id": "1fded00738610167d490f582677ba300",
        "phone_number": "+1 914-552-7876",
        "phone_code": "1",
        "primary": True,
    }

    # Patch `get_workday_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.workday.get_home_phones.get_workday_client"
    ) as mock_workday_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_workday_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "data": [
                {
                    "id": test_data["phone_id"],
                    "descriptor": test_data["phone_number"],
                    "countryPhoneCode": {"countryPhoneCode": test_data["phone_code"]},
                    "usage": {"primary": test_data["primary"]},
                }
            ],
        }

        # Get home phones
        response = get_home_phones(person_id=test_data["person_id"])

        # Ensure that get_home_phones() executed and returned proper values
        assert response
        assert len(response.home_phone_numbers)
        assert response.home_phone_numbers[0].phone_id == test_data["phone_id"]
        assert response.home_phone_numbers[0].phone_number == test_data["phone_number"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            url=f"api/person/v4/{mock_client.tenant_name}/people/{test_data['person_id']}/homePhones"
        )
