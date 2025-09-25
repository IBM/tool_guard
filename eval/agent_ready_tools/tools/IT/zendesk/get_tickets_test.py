from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.zendesk.get_tickets import Ticket, zendesk_get_tickets


def test_get_tickets_first_item() -> None:
    """Tests that the first Zendesk ticket in the response matches the expected data."""

    # Define test data
    test_data = {
        "description": "Test WO",
        "status": "open",
        "priority": "low",
        "subject": "Test WO",
        "created_at": "2025-06-27T12:29:00Z",
    }
    ticket_id = 184924
    requester_id = 382203429554
    submitter_id = 382203429554
    organization_id = 6159249256345

    # Inputs and expected pagination values
    per_page = 5
    page = 1
    output_page = None
    output_per_page = None

    with patch(
        "agent_ready_tools.tools.IT.zendesk.get_tickets.get_zendesk_client"
    ) as mock_get_client:
        # Setup mock client and response
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get_request.side_effect = [
            {
                "ticket_fields": [
                    {"id": 21583935524761, "title": "Component"},
                    {"id": 21959434346521, "title": "Is offboarding request"},
                    {"id": 21959543171737, "title": "Employee Email"},
                    {"id": 22172871394713, "title": "Awaiting customer response"},
                    {"id": 48530406607001, "title": "Asset"},
                    {"id": 48664164614937, "title": "custom_field_test"},
                    {"id": 48671102770201, "title": "Agentdescription"},
                ]
            },
            {
                "results": [
                    {
                        "id": ticket_id,
                        "description": test_data["description"],
                        "status": test_data["status"],
                        "requester_id": requester_id,
                        "submitter_id": submitter_id,
                        "organization_id": organization_id,
                        "priority": test_data["priority"],
                        "subject": test_data["subject"],
                        "created_at": test_data["created_at"],
                        "custom_fields": [
                            {"id": 21583935524761, "value": "accessories"},
                            {"id": 21959434346521, "value": False},
                            {"id": 21959543171737, "value": None},
                            {"id": 22172871394713, "value": True},
                            {"id": 48530406607001, "value": None},
                            {"id": 48664164614937, "value": True},
                            {"id": 48671102770201, "value": None},
                        ],
                    }
                ],
                "users": [
                    {
                        "id": requester_id,
                        "name": "Agent",
                    }
                ],
                "organizations": [
                    {
                        "id": organization_id,
                        "name": "New Org1",
                    }
                ],
                "next_page": None,
            },
        ]

        # Call the function
        response = zendesk_get_tickets(per_page=per_page, page=page)

        # Expected first ticket
        expected_first_ticket = Ticket(
            ticket_id=str(ticket_id),
            description=test_data["description"],
            status=test_data["status"],
            subject=test_data["subject"],
            created_at=test_data["created_at"],
            assignee_name=None,
            submitter_name="Agent",
            requester_name="Agent",
            organization_name="New Org1",
            group_name=None,
            priority=test_data["priority"],
            custom_fields={
                "Component": "accessories",
                "Is offboarding request": False,
                "Employee Email": None,
                "Awaiting customer response": True,
                "Asset": None,
                "custom_field_test": True,
                "Agentdescription": None,
            },
        )

        # Assertions
        assert response.tickets[0] == expected_first_ticket
        assert response.page == output_page
        assert response.per_page == output_per_page

        # Assert correct API calls
        mock_client.get_request.assert_any_call(entity="ticket_fields")
        mock_client.get_request.assert_any_call(
            entity="search",
            params={
                "query": "type:ticket",
                "per_page": per_page,
                "page": page,
                "include": "tickets(users,organizations,groups)",
            },
        )
