from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.oracle_hcm.create_home_address import (
    create_home_address,
)


def test_create_home_address() -> None:
    """Test that an address can be created successfully by the `create_home_address` tool."""

    # Define test data:
    test_data = {
        "worker_id": "00020000000EACED00057708000110D93445B0480000004AAC",
        "address_line_1": "south whales, plot no:4/87",
        "city": "San Jose",
        "postal_code": "95122",
        "state": "CA",
        "country": "US",
        "address_type": "HOME",
    }

    # Patch `get_oracle_hcm_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.oracle_hcm.create_home_address.get_oracle_hcm_client"
    ) as mock_get_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.post_request.return_value = {
            "AddressLine1": test_data["address_line_1"],
            "TownOrCity": test_data["city"],
            "PostalCode": test_data["postal_code"],
            "Region2": test_data["state"],
            "Country": test_data["country"],
        }

        # Create home address
        response = create_home_address(
            worker_id=test_data["worker_id"],
            address_type=test_data["address_type"],
            address_line_1=test_data["address_line_1"],
            city=test_data["city"],
            postal_code=test_data["postal_code"],
            state=test_data["state"],
            country=test_data["country"],
        )

        # Ensure that create_home_address() executed and returned proper values
        assert response
        assert response.address_line_1 == test_data["address_line_1"]

        # Ensure the API call was made with expected parameters
        mock_client.post_request.assert_called_once_with(
            entity=f"workers/{test_data['worker_id']}/child/addresses",
            payload={
                "AddressType": test_data["address_type"],
                "AddressLine1": test_data["address_line_1"],
                "PostalCode": test_data["postal_code"],
                "TownOrCity": test_data["city"],
                "Region2": test_data["state"],
                "Country": test_data["country"],
            },
        )
