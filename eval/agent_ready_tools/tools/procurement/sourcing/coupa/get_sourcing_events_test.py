from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.sourcing.coupa.get_sourcing_events import (
    CoupaQuoteRequest,
    coupa_get_sourcing_events,
)


def test_coupa_get_sourcing_events() -> None:
    """Test the get_sourcing_events tool."""

    # Define test data
    test_data = {
        "id": "123",
        "description": "Office Supplies RFP",
        "event-type": "rfp",
        "state": "new",
        "start-time": "2025-04-01T09:00:00Z",
        "end-time": "2025-04-10T17:00:00Z",
        "created-at": "2025-03-31T12:00:00Z",
    }

    # Patch get_coupa_client to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.sourcing.coupa.get_sourcing_events.get_coupa_client"
    ) as mock_coupa_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_coupa_client.return_value = mock_client
        mock_client.get_request_list.return_value = [test_data]

        # Call the function under test
        response = coupa_get_sourcing_events(event_type="rfp").content

        # Assertions
        assert response
        assert len(response) == 1

        event = response[0]
        assert isinstance(event, CoupaQuoteRequest)
        assert event.event_id == int(test_data["id"])
        assert event.event_name == test_data["description"]
        assert event.event_type == test_data["event-type"]
        assert event.state == test_data["state"]
        assert event.start_date == test_data["start-time"]
        assert event.end_date == test_data["end-time"]
        assert event.created_at == test_data["created-at"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request_list.assert_called_once_with(
            resource_name="quote_requests",
            params={
                "event-type": "rfp",
                "fields": '["id","description","created-at","start-time","state","end-time","event-type"]',
            },
        )


def test_coupa_get_sourcing_events_with_name() -> None:
    """Test the get_sourcing_events tool using one of the optional parameter event name."""

    # Define test data
    test_data = {
        "id": "266",
        "description": "Coding Services - SQL",
        "event-type": "rfp",
        "state": "test_complete",
        "start-time": "2015-07-15T09:38:49-07:00",
        "end-time": "2015-07-16T17:00:00-07:00",
        "created-at": "2015-07-15T09:34:55-07:00",
    }

    # Patch get_coupa_client to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.sourcing.coupa.get_sourcing_events.get_coupa_client"
    ) as mock_coupa_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_coupa_client.return_value = mock_client
        mock_client.get_request_list.return_value = [test_data]

        # Call the function under test
        response = coupa_get_sourcing_events(
            event_type="rfp", event_name="Coding Services - SQL"
        ).content

        # Assertions
        assert response
        assert len(response) == 1

        event = response[0]
        assert isinstance(event, CoupaQuoteRequest)
        assert event.event_id == int(test_data["id"])
        assert event.event_name == test_data["description"]
        assert event.event_type == test_data["event-type"]
        assert event.state == test_data["state"]
        assert event.start_date == test_data["start-time"]
        assert event.end_date == test_data["end-time"]
        assert event.created_at == test_data["created-at"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request_list.assert_called_once_with(
            resource_name="quote_requests",
            params={
                "event-type": "rfp",
                "fields": '["id","description","created-at","start-time","state","end-time","event-type"]',
                "description": "Coding Services - SQL",
            },
        )
