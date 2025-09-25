from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.servicenow.get_tickets import get_tickets


def test_get_tickets() -> None:
    """Test that the `get_tickets` function returns the expected response."""

    # Define test data:
    test_data = {
        "number": "TKT0010350",
        "id": "73148c9683542650e73115a6feaad39d",
        "due_date": "2025-03-27 07:10:19",
        "assignment_group": "Analytics setting manager",
        "assigned_to_user": "System user",
        "comments_and_work_notes": "Hello this is to test comments and work notes",
        "created_on": "2025-06-19 07:28:01",
        "opened_at": "2025-06-19 07:28:01",
        "closed_at": "2025-06-25 07:28:01",
        "priority": "1",
        "limit": 10,
        "skip": 0,
    }

    # Patch `get_servicenow_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.servicenow.get_tickets.get_servicenow_client"
    ) as mock_servicenow_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_servicenow_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "result": [
                {
                    "sys_id": test_data["id"],
                    "number": test_data["number"],
                    "due_date": test_data["due_date"],
                    "assignment_group": test_data["assignment_group"],
                    "assigned_to": test_data["assigned_to_user"],
                    "comments_and_work_notes": test_data["comments_and_work_notes"],
                    "priority": test_data["priority"],
                    "sys_created_on": test_data["created_on"],
                    "opened_at": test_data["opened_at"],
                    "closed_at": test_data["closed_at"],
                    "state": "1",
                    "short_description": "nothing",
                },
            ],
        }

        # Get tickets
        response = get_tickets(search=f"number={test_data['id']}")

        # Ensure that get_tickets() executed and returned proper values
        assert response
        assert len(response.tickets)
        assert response.tickets[0].system_id == test_data["id"]
        assert response.tickets[0].ticket_number == test_data["number"]
        assert response.tickets[0].due_date == test_data["due_date"]
        assert response.tickets[0].assignment_group == test_data["assignment_group"]
        assert response.tickets[0].assigned_to_user == test_data["assigned_to_user"]
        assert response.tickets[0].comments_and_work_notes == test_data["comments_and_work_notes"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            entity="ticket",
            params={
                "sysparm_query": f"number={test_data['id']}",
                "sysparm_display_value": True,
                "sysparm_limit": test_data["limit"],
                "sysparm_offset": test_data["skip"],
            },
        )
