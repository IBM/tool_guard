from typing import Any
from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.purchase_support.coupa.get_shipping_terms import (
    coupa_get_shipping_terms,
)


def test_coupa_get_shipping_terms() -> None:
    """Test that the `get_shipping_terms` return the expected response."""
    # Define Test Data
    test_data: list[dict[str, Any]] = [
        {"id": 1, "code": "FOB", "active": True},
        {"id": 2, "code": "CIF", "active": False},
    ]

    # Patch `get_coupa_client` to return mock client
    with patch(
        "agent_ready_tools.tools.procurement.purchase_support.coupa.get_shipping_terms.get_coupa_client"
    ) as mock_coupa_client:

        # create mock client instance
        mock_client = MagicMock()
        mock_coupa_client.return_value = mock_client
        mock_client.get_request_list.return_value = test_data

        response = coupa_get_shipping_terms().content

        # assert
        assert response
        assert len(response.shipping_terms_list) == 2
        assert response.shipping_terms_list[0].shipping_code == test_data[0]["code"]
        assert response.shipping_terms_list[1].shipping_code == test_data[1]["code"]

        # Ensure that the get_shipping_terms() execute and return the expected results
        mock_client.get_request_list.assert_called_once_with(
            resource_name="shipping_terms", params={"active": True}
        )
