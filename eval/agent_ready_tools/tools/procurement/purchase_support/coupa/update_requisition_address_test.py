from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.purchase_support.coupa.purchase_support_dataclasses import (
    CoupaAddress,
)
from agent_ready_tools.tools.procurement.purchase_support.coupa.update_requisition_address import (
    coupa_update_requisition_address,
)


def test_coupa_update_address_requisition() -> None:
    """Test that the `update_address_to_requisition_coupa` function returns the expected
    response."""

    # Define test data:
    test_data = {
        "requisition_id": 555,
        "street1": "555 Bailey Ave",
        "city": "San Jose",
        "postal_code": "95141",
        "state": "CA",
        "country_code": "USA",
    }

    mock_address_id = 55555
    mock_address = {
        "street1": test_data["street1"],
        "city": test_data["city"],
        "state": test_data["state"],
        "postal-code": test_data["postal_code"],
        "country": {
            "code": test_data["country_code"],
        },
    }

    # Patch `get_coupa_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.purchase_support.coupa.update_requisition_address.get_coupa_client"
    ) as mock_coupa_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_coupa_client.return_value = mock_client
        # get requisition and then get the shipping address of it
        mock_client.get_request.return_value = {
            "ship-to-address": mock_address | {"id": mock_address_id}
        }

        mock_client.put_request.return_value = mock_address | {"id": mock_address_id}

        # Add address to a requisition
        response: CoupaAddress = coupa_update_requisition_address(**test_data).content

        # Ensure that update_address_by_requisition_id executed and returned proper values
        assert response
        assert response.id == mock_address_id
        assert response.street1 == test_data["street1"]

        mock_client.get_request.assert_called_once_with(
            resource_name=f"requisitions/{test_data['requisition_id']}"
        )

        # Ensure the API call was made with expected parameters
        mock_client.put_request.assert_called_once_with(
            resource_name=f"addresses/{mock_address_id}", payload=mock_address
        )
