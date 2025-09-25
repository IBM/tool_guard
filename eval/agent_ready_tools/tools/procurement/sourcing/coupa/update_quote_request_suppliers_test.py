from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.sourcing.coupa.update_quote_request_suppliers import (
    coupa_update_quote_request_suppliers,
)


def test_coupa_update_quote_request_suppliers() -> None:
    """Test that `update_quote_request_suppliers` function returns the expected response."""

    # Define test data
    quote_request_id = 123
    supplier_name = "Sign"
    supplier_contact_name = "TESTING Response"
    supplier_email = "eshwar_test@coupa.com"

    expected_payload = {
        "quote-suppliers": [
            {"name": supplier_name, "contact-name": supplier_contact_name, "email": supplier_email}
        ]
    }

    # Patch `get_coupa_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.sourcing.coupa.update_quote_request_suppliers.get_coupa_client"
    ) as mock_get_client:
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        # Simulate Coupa returning the updated object
        mock_client.put_request.return_value = {"id": quote_request_id}

        # Update quote requests general info
        result = coupa_update_quote_request_suppliers(
            quote_request_id=quote_request_id,
            supplier_name=supplier_name,
            supplier_contact_name=supplier_contact_name,
            supplier_email=supplier_email,
        ).content

        # Ensure that update_quote_request_suppliers() executed and returned True to condition
        assert result is True

        # Ensure the API call was made with expected parameters and payload
        mock_client.put_request.assert_called_once_with(
            resource_name=f"quote_requests/{quote_request_id}",
            payload=expected_payload,
        )
