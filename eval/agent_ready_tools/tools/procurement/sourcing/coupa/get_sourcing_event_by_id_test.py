from typing import Any, Dict
from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.sourcing.coupa.common_classes_sourcing import (
    CoupaCurrency,
    CoupaQuoteRequests,
)
from agent_ready_tools.tools.procurement.sourcing.coupa.get_sourcing_event_by_id import (
    coupa_get_sourcing_event_by_id,
)


def test_coupa_get_sourcing_event_by_id() -> None:
    """Test the get_sourcing_event_by_id tool."""
    quote_request_id = 123
    # Define test data
    test_data: Dict[str, Any] = {
        "id": 123,
        "event-type": "rfp",
        "description": "Test event",
        "state": "open",
        "start-time": "2024-04-01T00:00:00Z",
        "end-time": "2024-04-10T00:00:00Z",
        "submit-time": "2024-04-02T00:00:00Z",
        "currency": {"code": "USD"},
        "created-by": {"id": 1, "fullname": "John Doe", "email": "john@example.com"},
        "updated-by": {"id": 2, "fullname": "Jane Smith", "email": "jane@example.com"},
        "quote-suppliers": [
            {"id": 1001, "name": "Supplier A"},
            {"id": 1002, "name": "Supplier B"},
        ],
        "commodity": {"id": 501, "name": "Hardware"},
    }

    # Patch get_coupa_client to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.sourcing.coupa.get_sourcing_event_by_id.get_coupa_client"
    ) as mock_coupa_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_coupa_client.return_value = mock_client
        mock_client.get_request.return_value = test_data

        # Call the function under test
        event = coupa_get_sourcing_event_by_id(quote_request_id, event_type="rfp").content

        # Assertions
        assert event
        assert isinstance(event, CoupaQuoteRequests)

        assert event.id == test_data["id"]
        assert event.event_type == test_data["event-type"]
        assert event.state == test_data["state"]
        assert event.start_time == test_data["start-time"]
        assert event.end_time == test_data["end-time"]
        assert event.submit_time == test_data["submit-time"]
        assert event.currency == CoupaCurrency(test_data["currency"]["code"])

        mock_client.get_request.assert_called_once_with(
            resource_name=f"quote_requests/{test_data["id"]}",
            params={"event-type": f"{test_data["event-type"]}"},
        )
