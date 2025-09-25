from typing import Any
from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.zendesk.get_ticket_statuses import TicketStatus, get_ticket_statuses


def test_get_ticket_statuses_first_item() -> None:
    """Tests that the first ticket status in the response matches the expected data."""

    # Define test data
    test_data: dict[str, Any] = {
        "id": 2611046,
        "name": "New",
        "status": "New",
    }

    with patch(
        "agent_ready_tools.tools.IT.zendesk.get_ticket_statuses.get_zendesk_client"
    ) as mock_get_client:
        # Setup mock client and response
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "custom_statuses": [
                {
                    "id": test_data["id"],
                    "agent_label": test_data["name"],
                }
            ]
        }

        # Call the function
        response = get_ticket_statuses(status=test_data["status"])

        # Expected first ticket status
        expected_first_status = TicketStatus(
            id=test_data["id"],
            name=test_data["name"],
        )

        # Assertions
        assert response.ticket_statuses[0] == expected_first_status

        # Assert correct API call
        mock_client.get_request.assert_called_once_with(
            entity="custom_statuses", params={"status_categories": test_data["status"]}
        )
