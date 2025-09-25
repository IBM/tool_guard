from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.sourcing.coupa.update_quote_request_timeline import (
    coupa_update_quote_request_timeline,
)


def test_coupa_update_quote_request_timeline_success_all_fields() -> None:
    """When all parameters are provided, the payload keys and values should match the conversion."""
    quote_request_id = 1001
    start_date = "2025-05-30"
    end_date = "2025-06-15"
    start_on_submit = False

    # Expected converted values:
    expected_start = "05/30/25 12:00 AM -0700"
    expected_end = "06/15/25 12:00 AM -0700"

    mock_client = MagicMock()
    mock_client.put_request.return_value = {"id": quote_request_id}

    with patch(
        "agent_ready_tools.tools.procurement.sourcing.coupa.update_quote_request_timeline.get_coupa_client"
    ) as mock_coupa_client:
        mock_client = MagicMock()
        mock_coupa_client.return_value = mock_client
        mock_client.put_request.return_value = {"id": quote_request_id}
        result = coupa_update_quote_request_timeline(
            quote_request_id=quote_request_id,
            start_time=start_date,
            end_time=end_date,
            start_on_submit=start_on_submit,
        ).content

        assert result

        mock_client.put_request.assert_called_once_with(
            resource_name=f"quote_requests/{quote_request_id}",
            payload={
                "start-time": expected_start,
                "end-time": expected_end,
                "start-on-submit": start_on_submit,
            },
        )
