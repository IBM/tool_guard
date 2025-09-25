from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.purchase_support.coupa.add_address_to_requisition import (
    coupa_add_address_to_requisition,
)
from agent_ready_tools.tools.procurement.purchase_support.coupa.get_requisition_by_id_test import (
    mock_requisition_response,
)
from agent_ready_tools.tools.procurement.purchase_support.coupa.purchase_support_dataclasses import (
    CoupaAddress,
)


def test_coupa_add_address_to_requisition() -> None:
    """Test that the `add_address_to_requisition_coupa` function returns the expected response."""

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
        "location-code": f"ship-to-{test_data["requisition_id"]}",
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
        "agent_ready_tools.tools.procurement.purchase_support.coupa.add_address_to_requisition.get_coupa_client"
    ) as mock_coupa_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_coupa_client.return_value = mock_client
        mock_client.get_request.return_value = mock_requisition_response()
        mock_client.post_request.return_value = mock_address | {"id": mock_address_id}

        mock_client.put_request.return_value = {
            "ship-to-address": mock_address | {"id": mock_address_id}
        }

        # Add address to a requisition
        response: CoupaAddress = coupa_add_address_to_requisition(**test_data).content

        # Ensure that add_address_by_requisition_id executed and returned proper values
        assert response
        assert response.id == mock_address_id
        assert response.street1 == test_data["street1"]

        mock_client.post_request.assert_called_once_with(
            resource_name="addresses", payload=mock_address
        )

        # Ensure the API call was made with expected parameters
        mock_client.put_request.assert_called_once_with(
            resource_name=f"requisitions/{test_data['requisition_id']}",
            payload={"ship-to-address": {"id": mock_address_id}},
        )
