from typing import Any
from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.zendesk.zendesk_schemas import TicketPriority
from agent_ready_tools.tools.IT.zendesk.zendesk_update_ticket import zendesk_update_ticket


def test_zendesk_update_ticket() -> None:
    """Verifies that the `zendesk_update_ticket` tool can successfully update a Zendesk ticket."""

    # Define test data:
    test_data: dict[str, Any] = {
        "ticket_id": 184933,
        "ticket_status": "pending",
        "ticket_priority": TicketPriority.NORMAL,
        "ticket_subject": "Updated subject from unit test",
        "assignee_id": 382203429554,
        "ticket_comment": "Unit test comment update.",
        "group_id": 987654321,
    }

    # Patch the Zendesk client
    with patch(
        "agent_ready_tools.tools.IT.zendesk.zendesk_update_ticket.get_zendesk_client"
    ) as mock_get_client:
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        # Define expected API response
        mock_client.put_request.return_value = {
            "ticket": {
                "id": test_data["ticket_id"],
                "status": test_data["ticket_status"],
                "priority": test_data["ticket_priority"].value,
                "subject": test_data["ticket_subject"],
                "assignee_id": test_data["assignee_id"],
            }
        }

        # Update a ticket
        response = zendesk_update_ticket(
            ticket_id=test_data["ticket_id"],
            ticket_status=test_data["ticket_status"],
            ticket_priority=test_data["ticket_priority"],
            ticket_subject=test_data["ticket_subject"],
            assignee_id=test_data["assignee_id"],
            ticket_comment=test_data["ticket_comment"],
            group_id=test_data["group_id"],
        )

        # Ensure that zendesk_update_ticket() executed and returned proper values
        assert response is not None
        assert response.ticket_id == test_data["ticket_id"]
        assert response.ticket_status == test_data["ticket_status"]
        assert response.ticket_priority == test_data["ticket_priority"]
        assert response.ticket_subject == test_data["ticket_subject"]
        assert response.assignee_id == test_data["assignee_id"]

        # Ensure API call was made with correct payload
        mock_client.put_request.assert_called_once_with(
            entity=f"tickets/{test_data['ticket_id']}",
            payload={
                "ticket": {
                    "status": test_data["ticket_status"],
                    "priority": test_data["ticket_priority"].value,
                    "subject": test_data["ticket_subject"],
                    "assignee_id": test_data["assignee_id"],
                    "comment": {"body": test_data["ticket_comment"]},
                    "group_id": test_data["group_id"],
                }
            },
        )
