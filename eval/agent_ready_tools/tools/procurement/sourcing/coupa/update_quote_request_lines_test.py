from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.sourcing.coupa.update_quote_request_lines import (
    coupa_update_quote_request_lines,
)


def test_coupa_update_quote_request_lines() -> None:
    """Test that `update_quote_request_lines` function returns the expected response."""

    # Define test data
    test_data = {
        "quote_request_id": 123,
        "line_type": "item",
        "line_quantity": "3.0",
        "line_description": "10x15 bold signs",
    }

    expected_payload = {
        "lines": [
            {
                "type": "QuoteRequestQuantityLine",
                "quantity": "3.0",
            }
        ]
    }

    # Patch `get_coupa_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.sourcing.coupa.update_quote_request_lines.get_coupa_client"
    ) as mock_coupa_client:
        mock_client = MagicMock()
        mock_coupa_client.return_value = mock_client
        mock_client.put_request.return_value = {"id": test_data["quote_request_id"]}

        # Update quote requests general info
        result = coupa_update_quote_request_lines(
            quote_request_id=test_data["quote_request_id"],
            line_type=test_data["line_type"],
            line_quantity=test_data["line_quantity"],
        ).content

        # Ensure that update_quote_request_lines() executed and returned True to condition
        assert result is True

        # Ensure the API call was made with expected parameters and payload
        mock_client.put_request.assert_called_once_with(
            resource_name=f"quote_requests/{test_data['quote_request_id']}",
            payload=expected_payload,
        )
