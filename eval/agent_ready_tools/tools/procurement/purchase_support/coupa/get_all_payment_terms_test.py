from typing import Any
from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.purchase_support.coupa.get_all_payment_terms import (
    coupa_get_all_payment_terms,
)


def test_coupa_get_all_payment_terms() -> None:
    """Test that the `get_all_payment_terms` function returns the expected response."""

    test_data: list[dict[str, Any]] = [
        {"id": 1, "code": "transfer", "active": True},
        {"id": 2, "code": "Net 30", "active": True},
        {"id": 3, "code": "Net 15", "active": True},
    ]

    # Patch `get_coupa_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.purchase_support.coupa.get_all_payment_terms.get_coupa_client"
    ) as mock_coupa_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_coupa_client.return_value = mock_client
        mock_client.get_request_list.return_value = test_data

        # Get all payment terms
        response = coupa_get_all_payment_terms().content

        # Ensure that get_all_departments() executed and returned proper values
        assert response
        assert response.payment_terms_list and len(response.payment_terms_list) == 3
        assert response.payment_terms_list[0].payment_code == test_data[0]["code"]
        assert response.payment_terms_list[1].payment_code == test_data[1]["code"]
        assert response.payment_terms_list[2].payment_active_status == test_data[2]["active"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request_list.assert_called_once_with(resource_name="payment_terms")
