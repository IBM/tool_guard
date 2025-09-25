from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.oracle_hcm.update_phone_number import (
    update_phone_number,
)


def test_update_phone_number() -> None:
    """Test that the `update_phone_number` function returns the expected response."""

    # Define test data:
    test_data = {
        "worker_id": "00020000000EACED00057708000110D93445B0480000004AAC",
        "phone_id": 999999999999999,
        "phone_number": "675-5267",
        "country_code_number": "+1",
        "area_code": "661",
        "phone_type": "M",
        "legislation_code": "US",
    }

    # Patch `get_oracle_hcm_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.oracle_hcm.update_phone_number.get_oracle_hcm_client"
    ) as mock_get_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.update_request.return_value = {
            "PhoneNumber": test_data["phone_number"],
            "CountryCodeNumber": test_data["country_code_number"],
            "AreaCode": test_data["area_code"],
            "PhoneId": test_data["phone_id"],
            "PhoneType": test_data["phone_type"],
        }

        # Update user's phone number
        response = update_phone_number(
            worker_id=test_data["worker_id"],
            phone_id=test_data["phone_id"],
            phone_number=test_data["phone_number"],
            area_code=test_data["area_code"],
            phone_type=test_data["phone_type"],
            country_code=test_data["country_code_number"],
            legislation_code=test_data["legislation_code"],
        )

        # Ensure that update_phone_number() executed and returned proper values
        assert response
        assert response.phone_number == test_data["phone_number"]
        assert response.area_code == test_data["area_code"]
        assert response.country_code == test_data["country_code_number"]

        # Ensure the API call was made with expected parameters
        mock_client.update_request.assert_called_once_with(
            entity=f"workers/{test_data['worker_id']}/child/phones/{test_data['phone_id']}",
            payload={
                "PhoneNumber": test_data["phone_number"],
                "CountryCodeNumber": test_data["country_code_number"],
                "AreaCode": test_data["area_code"],
                "PhoneType": test_data["phone_type"],
                "LegislationCode": test_data["legislation_code"],
            },
        )
