from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.servicenow.create_a_ticket import create_a_ticket


def test_create_a_ticket() -> None:
    """Verify that the `create_a_ticket` tool can successfully create a ticket in ServiceNow."""

    # Define test data:
    test_data = {
        "short_description": "Creating a ticket",
        "assignment_group": "Analytics Settings Managers",
        "parent_task_number": "TASK0022543",
        "description": "Creating a ticket in ServiceNow",
        "priority": "2",
        "ticket_number": "TASK0022544",
        "http_code": 201,
    }

    # Patch `get_servicenow_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.servicenow.create_a_ticket.get_servicenow_client"
    ) as mock_servicenow_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_servicenow_client.return_value = mock_client
        mock_client.post_request.return_value = {
            "result": {
                "number": test_data["ticket_number"],
                "short_description": test_data["short_description"],
            },
            "status_code": test_data["http_code"],
        }

        # Create a ticket
        response = create_a_ticket(
            short_description=test_data["short_description"],
            assignment_group=test_data["assignment_group"],
            parent_task_number=test_data["parent_task_number"],
            description=test_data["description"],
            priority=test_data["priority"],
        )

        # Ensure that create_a_ticket() executed and returned proper values
        assert response
        assert response.http_code == test_data["http_code"]
        assert response.ticket_number == test_data["ticket_number"]
        assert response.short_description == test_data["short_description"]

        # Ensure the API call was made with expected parameters
        mock_client.post_request.assert_called_once_with(
            entity="ticket",
            payload={
                "short_description": test_data["short_description"],
                "assignment_group": test_data["assignment_group"],
                "parent": test_data["parent_task_number"],
                "description": test_data["description"],
                "priority": test_data["priority"],
            },
        )
