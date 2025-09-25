from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.purchase_support.coupa.get_address_by_id import (
    coupa_get_address_by_id,
)
from agent_ready_tools.tools.procurement.purchase_support.coupa.purchase_support_dataclasses import (
    CoupaAddress,
)


def test_coupa_get_address_by_id() -> None:
    """Test that the `coupa_get_address_by_id` function returns the expected response."""

    # Define test data:
    test_data = {
        "requisition_id": 555,
        "street": "555 Bailey Ave",
        "city": "San Jose",
        "postal_code": "95141",
        "state": "CA",
        "country_code": "USA",
    }

    mock_address_id = 55555
    mock_address = {
        "id": mock_address_id,
        "location-code": f"ship-to-{test_data["requisition_id"]}",
        "street1": test_data["street"],
        "city": test_data["city"],
        "state": test_data["state"],
        "postal-code": test_data["postal_code"],
        "country": {
            "code": test_data["country_code"],
        },
    }

    # Patch `get_coupa_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.purchase_support.coupa.get_address_by_id.get_coupa_client"
    ) as mock_coupa_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_coupa_client.return_value = mock_client

        mock_client.get_request.return_value = mock_address

        # Get address of a requisition
        response: CoupaAddress = coupa_get_address_by_id(mock_address_id).content

        # Ensure that get_address_by_requisition_id executed and returned proper values
        assert response
        assert response.id == mock_address_id
        assert response.street1 == test_data["street"]
