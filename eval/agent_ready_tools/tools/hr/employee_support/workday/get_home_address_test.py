from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.workday.get_home_address import get_home_address


def test_get_home_address() -> None:
    """Test that the `get_home_address` function returns the expected response."""

    # Define test data:
    test_data = {
        "person_id": "d3fd6c7cdbf1101b037a55f03aea0c20",
        "address_id": "d3fd6c7cdbf1101b037a564a1aba0c28",
        "address_line_1": "Blue Avenue 1",
        "city": "San Francisco",
        "postal_code": "77-777",
        "country_id": "1",
        "country": "United States of America",
        "state_id": "1",
        "state": "California",
    }

    # Patch `get_workday_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.workday.get_home_address.get_workday_client"
    ) as mock_workday_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_workday_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "data": [
                {
                    "id": test_data["address_id"],
                    "addressLine1": test_data["address_line_1"],
                    "city": test_data["city"],
                    "postalCode": test_data["postal_code"],
                    "countryRegion": {
                        "id": test_data["state_id"],
                        "descriptor": test_data["state"],
                    },
                    "country": {
                        "id": test_data["country_id"],
                        "descriptor": test_data["country"],
                    },
                }
            ],
        }

        # Get home address
        response = get_home_address(person_id=test_data["person_id"])

        # Ensure that get_home_address() executed and returned proper values
        assert response
        assert len(response.home_addresses) > 0
        response = response.home_addresses[0]
        assert response.address_id == test_data["address_id"]
        assert response.address_line_1 == test_data["address_line_1"]
        assert response.city == test_data["city"]
        assert response.postal_code == test_data["postal_code"]
        assert response.state_id == test_data["state_id"]
        assert response.country_id == test_data["country_id"]
        assert response.state == test_data["state"]
        assert response.country == test_data["country"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            url=f"api/person/v4/{mock_client.tenant_name}/people/{test_data['person_id']}/homeAddresses"
        )
