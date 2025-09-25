from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.zendesk.zendesk_create_a_ticket import zendesk_create_a_ticket


def test_update_an_event() -> None:
    """Verifies that the ticket is created successfully by the `create_a_ticket` tool."""

    # Create the test data
    test_data = {
        "ticket_comment": "This ticket comment is for testing purpose.",
        "ticket_subject": "Test ticket comment.",
        "ticket_priority": "NORMAL",
        "ticket_id": 184934,
        "group_id": 6346935417881,
        "ticket_type": "TASK",
        "ticket_component": "CORE_ITEM",
    }

    # Patch the microsoft client with the mock object
    with patch(
        "agent_ready_tools.tools.IT.zendesk.zendesk_create_a_ticket.get_zendesk_client"
    ) as mock_zendesk_client:

        # Create a mock client
        mock_client = MagicMock()
        mock_zendesk_client.return_value = mock_client
        mock_client.post_request.return_value = {
            "id": test_data["ticket_id"],
            "description": test_data["ticket_comment"],
            "subject": test_data["ticket_subject"],
            "priority": test_data["ticket_priority"],
            "status_code": 200,
        }

        # Create a ticket
        response = zendesk_create_a_ticket(
            ticket_comment=test_data["ticket_comment"],
            ticket_subject=test_data["ticket_subject"],
            ticket_priority=test_data["ticket_priority"],
            group_id=test_data["group_id"],
            ticket_type=test_data["ticket_type"],
            ticket_component=test_data["ticket_component"],
        )

        assert response
        assert response.ticket_id is not None

        # Ensure the API call was made with expected parameters
        mock_client.post_request.assert_called_once_with(
            entity="tickets",
            payload={
                "ticket": {
                    "comment": {
                        "body": test_data["ticket_comment"],
                    },
                    "subject": test_data["ticket_subject"],
                    "priority": "normal",
                    "group_id": test_data["group_id"],
                    "type": "Task",
                    "tags": ["Core Item"],
                }
            },
        )
