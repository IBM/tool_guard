from typing import Any
from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.purchase_support.coupa.get_all_addresses import (
    coupa_get_all_addresses,
)


def test_coupa_get_all_addresses() -> None:
    """Test that the `get_all_addresses` function returns the expected response."""

    test_data: list[dict[str, Any]] = [
        {
            "id": 231564,
            "location_code": None,
            "street1": "dfdff",
            "city": "sdsa",
            "state": None,
            "postal-code": "90908",
            "country": {"code": "IN", "name": "India"},
        },
        {
            "id": 231561,
            "location_code": "ship-to-5429",
            "street1": "lineaddress1",
            "city": "Elko",
            "state": "NV",
            "postal-code": "08551-3423",
            "country": {"code": "US", "name": "United States"},
        },
        {
            "id": 231560,
            "location_code": None,
            "street1": "555 bailey avenue",
            "city": "san jose",
            "state": None,
            "postal-code": "95147",
            "country": {"code": "US", "name": "United States"},
        },
    ]

    # Patch `get_coupa_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.purchase_support.coupa.get_all_addresses.get_coupa_client"
    ) as mock_coupa_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_coupa_client.return_value = mock_client
        mock_client.get_request_list.return_value = test_data

        # Get all addresses
        response = coupa_get_all_addresses().content

        # Ensure that get_all_addresses() executed and returned proper values
        assert response
        assert response and len(response.address_list) == 3
        assert response.address_list[0].id == test_data[0]["id"]
        assert response.address_list[1].state == test_data[1]["state"]
        assert response.address_list[2].street1 == test_data[2]["street1"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request_list.assert_called_once_with(
            resource_name="addresses",
            params={"limit": 10, "offset": 0, "order_by": "created-at", "dir": "desc"},
        )
