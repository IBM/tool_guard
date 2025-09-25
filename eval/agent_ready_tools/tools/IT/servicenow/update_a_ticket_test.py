from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.servicenow.update_a_ticket import update_a_ticket


def test_update_a_ticket() -> None:
    """Test that the `update_a_ticket` function returns the expected response."""

    # Define test data:
    test_data = {
        "ticket_number_system_id": "f3badb5b83e71210e73115a6feaad3f4",
        "description": "Hello World Test Description",
        "due_date": "2025-03-15",
        "short_description": "Hello short description",
        "assignment_group": "Analytics Settings Managers",
        "priority": "3",
        "state_code": "2",
        "comments": "Adding a comment in a ticket",
        "work_notes": "Adding a work note in a ticket",
        "http_code": 200,
    }

    # Patch `get_servicenow_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.servicenow.update_a_ticket.get_servicenow_client"
    ) as mock_servicenow_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_servicenow_client.return_value = mock_client
        mock_client.patch_request.return_value = {"status_code": test_data["http_code"]}

        # Update a ticket
        response = update_a_ticket(
            ticket_number_system_id=test_data["ticket_number_system_id"],
            description=test_data["description"],
            due_date=test_data["due_date"],
            short_description=test_data["short_description"],
            priority=test_data["priority"],
            state_code=test_data["state_code"],
            assignment_group=test_data["assignment_group"],
            comments=test_data["comments"],
            work_notes=test_data["work_notes"],
        )

        # Ensure that update_a_ticket() executed and returned proper values
        assert response
        assert response.http_code == 200

        # Ensure the API call was made with expected parameters
        mock_client.patch_request.assert_called_once_with(
            entity="ticket",
            entity_id=test_data["ticket_number_system_id"],
            payload={
                "description": test_data["description"],
                "due_date": test_data["due_date"],
                "short_description": test_data["short_description"],
                "assignment_group": test_data["assignment_group"],
                "priority": test_data["priority"],
                "state": test_data["state_code"],
                "comments": test_data["comments"],
                "work_notes": test_data["work_notes"],
            },
            params={"sysparm_display_value": True},
        )
