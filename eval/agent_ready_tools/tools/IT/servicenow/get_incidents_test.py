from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.servicenow.get_incidents import get_incidents


def test_get_incidents() -> None:
    """Test that the incidents can be retrieved by the `get_incidents` tool."""

    # Define test data:
    test_data = {
        "id": "INC0010456",
        "short_description": "New Tool code implementation test for Incident",
        "system_id": "52a400d683542650e73115a6feaad390",
        "assignment_group": "Analytics setting manager",
        "assigned_to_user": "System user",
        "comments_and_work_notes": "Hello this is to test comments and work notes",
        "caller_username": "survey user",
        "created_on": "2025-06-19 07:28:01",
        "opened_at": "2025-06-19 07:28:01",
        "closed_at": "2025-06-25 07:28:01",
        "limit": 10,
        "skip": 0,
    }

    # Patch `get_servicenow_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.servicenow.get_incidents.get_servicenow_client"
    ) as mock_servicenow_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_servicenow_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "result": [
                {
                    "number": test_data["id"],
                    "sys_id": test_data["system_id"],
                    "short_description": test_data["short_description"],
                    "description": test_data["short_description"],
                    "assignment_group": test_data["assignment_group"],
                    "assigned_to": test_data["assigned_to_user"],
                    "comments_and_work_notes": test_data["comments_and_work_notes"],
                    "caller_username": test_data["caller_username"],
                    "sys_created_on": test_data["created_on"],
                    "opened_at": test_data["opened_at"],
                    "closed_at": test_data["closed_at"],
                    "category": "Inquiry / Help",
                    "impact": "1 - High",
                    "urgency": "1 - High",
                    "state": "New",
                    "priority": "1 - Critical",
                },
            ],
        }

        # Get incidents
        response = get_incidents(search=f"number={test_data['id']}")

        # Ensure that get_incidents() executed and returned proper values
        assert response
        assert len(response.incidents)
        assert response.incidents[0].incident_number == test_data["id"]
        assert response.incidents[0].short_description == test_data["short_description"]
        assert response.incidents[0].assigned_to_user == test_data["assigned_to_user"]
        assert response.incidents[0].system_id == test_data["system_id"]
        assert response.incidents[0].assignment_group == test_data["assignment_group"]
        assert response.incidents[0].comments_and_work_notes == test_data["comments_and_work_notes"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            entity="incident",
            params={
                "sysparm_query": f"number={test_data['id']}",
                "sysparm_display_value": True,
                "sysparm_limit": test_data["limit"],
                "sysparm_offset": test_data["skip"],
            },
        )
