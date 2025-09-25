from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.oracle_hcm.get_address import get_address


def test_get_address() -> None:
    """Test that the `get_address` function returns the expected response."""

    # Define test data:
    test_data = {
        "worker_id": "00020000000EACED00057708000110D942344E6E0000004AAC",
        "address_type": "HOME",
        "address_id": "00020000000EACED00057708000110D94234E9F80000004AAC",
        "postal_code": "63005",
        "url": "https://example.dev.oraclepdemos.com:443/hcmRestApi/resources/11.12.13.14",
    }

    # Patch `get_oracle_hcm_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.oracle_hcm.get_address.get_oracle_hcm_client"
    ) as mock_get_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "items": [
                {
                    "AddressLine1": "Barlow, plot no 45/A",
                    "AddressLine2": None,
                    "TownOrCity": "Wildwood",
                    "Region1": "St Louis",
                    "Region2": "MO",
                    "Region3": None,
                    "PostalCode": test_data["postal_code"],
                    "Country": "US",
                    "PrimaryFlag": False,
                    "links": [
                        {
                            "href": f"{test_data['url']}/workers/{test_data['worker_id']}/addresses/{test_data['address_id']}",
                        }
                    ],
                }
            ]
        }

        # Get address
        response = get_address(
            worker_id=test_data["worker_id"], address_type=test_data["address_type"]
        ).address_details

        # Ensure that get_address() executed and returned proper values
        assert response
        assert len(response)
        assert response[0].address_uniq_id == test_data["address_id"]
        assert response[0].postal_code == test_data["postal_code"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            f"workers/{test_data['worker_id']}/child/addresses",
            q_expr=f"AddressType ={test_data['address_type']}",
        )
