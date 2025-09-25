from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.oracle_hcm.get_phones import (
    UserPhonesResponse,
    get_phones,
)


def test_get_phones() -> None:
    """Test that the `get_phones` function returns the expected response."""

    # Define test data:
    test_data = {
        "worker_id": "00020000000EACED00057708000110D93445B0480000004AAC",
        "phone_id": 999999999999999,
        "phone_type": "W1",
        "area_code": "222",
        "country_code": "1",
        "phone_number": "444-9999",
    }

    # Patch `get_oracle_hcm_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.oracle_hcm.get_phones.get_oracle_hcm_client"
    ) as mock_get_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "items": [
                {
                    "PhoneId": test_data["phone_id"],
                    "PhoneType": test_data["phone_type"],
                    "PhoneNumber": test_data["phone_number"],
                    "AreaCode": test_data["area_code"],
                    "CountryCodeNumber": test_data["country_code"],
                }
            ]
        }

        # Get phone IDs
        response: UserPhonesResponse = get_phones(test_data["worker_id"])

        # Ensure that get_phones() got executed properly and returned proper values
        assert response
        assert len(response.phones)
        assert response.phones[0].phone_id == test_data["phone_id"]
        assert response.phones[0].phone_number == test_data["phone_number"]
        assert response.phones[0].area_code == test_data["area_code"]
        assert response.phones[0].country_code == test_data["country_code"]
        assert response.phones[0].phone_type == test_data["phone_type"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            entity=f'workers/{test_data["worker_id"]}/child/phones'
        )
