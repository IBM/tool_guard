from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.sourcing.coupa.update_quote_request_general_info_by_id import (
    coupa_update_quote_request_general_info_by_id,
)


def test_coupa_update_quote_request_general_info_by_id() -> None:
    """Test that `update_quote_request_general_info_by_id` function returns the expected
    response."""

    # Define test data
    test_data = {
        "quote_request_id": 123,
        "event_type": "rfp",
        "comments": "comments",
        "commodity_name": "IT",
    }

    expected_payload = {
        "event-type": test_data["event_type"],
        "comments": test_data["comments"],
        "commodity": {"name": test_data["commodity_name"]},
    }

    # Patch `get_coupa_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.sourcing.coupa.update_quote_request_general_info_by_id.get_coupa_client"
    ) as mock_coupa_client:
        mock_client = MagicMock()
        mock_coupa_client.return_value = mock_client
        mock_client.put_request.return_value = {"id": test_data["quote_request_id"]}

        # Update quote requests general info
        result = coupa_update_quote_request_general_info_by_id(
            quote_request_id=test_data["quote_request_id"],
            commodity_name=test_data["commodity_name"],
            comments=test_data["comments"],
        ).content

        # Ensure that update_quote_request_general_info_by_id() executed and returned True to condition
        assert result

        # Ensure the API call was made with expected parameters and payload
        mock_client.put_request.assert_called_once_with(
            resource_name=f"quote_requests/{test_data['quote_request_id']}",
            payload=expected_payload,
        )
