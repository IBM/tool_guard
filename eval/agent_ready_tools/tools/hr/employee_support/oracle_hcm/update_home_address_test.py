from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.oracle_hcm.update_home_address import (
    update_home_address_oracle,
)


def test_update_home_addess() -> None:
    """Test that an address can be updated successfully by the `update_home_address` tool."""

    # Define test data:
    test_data = {
        "worker_id": "00020000000EACED00057708000110D942344E6E0000004AAC",
        "address_id": "00020000000EACED00057708000110D94234E9F80000004AAC",
        "postal_code": "63005",
        "address_line_1": "Barlow, plot no 45/A",
        "city": "Wildwood",
        "state_province_or_region": "NJ",
    }

    # Patch `get_oracle_hcm_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.oracle_hcm.update_home_address.get_oracle_hcm_client"
    ) as mock_get_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.update_request.return_value = {
            "AddressLine1": test_data["address_line_1"],
            "TownOrCity": test_data["city"],
            "PostalCode": test_data["postal_code"],
        }

        # Get Update home address
        response = update_home_address_oracle(
            worker_id=test_data["worker_id"],
            address_uniq_id=test_data["address_id"],
            address_line_1=test_data["address_line_1"],
            address_line_2=None,
            city=test_data["city"],
            postal_code=test_data["postal_code"],
            state_province_or_region=test_data["state_province_or_region"],
            is_primary_address=None,
        )

        # Ensure that get_address() executed and returned proper values
        assert response
        assert response.address_line_1 == test_data["address_line_1"]
        assert response.postal_code == test_data["postal_code"]
        assert response.city == test_data["city"]

        # Ensure the API call was made with expected parameters
        mock_client.update_request.assert_called_once_with(
            entity=f"workers/{test_data['worker_id']}/child/addresses/{test_data['address_id']}",
            payload={
                "AddressLine1": test_data["address_line_1"],
                "PostalCode": test_data["postal_code"],
                "TownOrCity": test_data["city"],
                "Region2": test_data["state_province_or_region"],
            },
        )
