from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.servicenow.create_an_incident import create_an_incident


def test_create_an_incident() -> None:
    """Test that incident can be created successfully by the `create_an_incident` tool."""

    # Define test data:
    test_data = {
        "short_description": "New Tool code implementation test for Database_Incident",
        "impact_value": "1",
        "urgency_value": "1",
        "incident_category": "Database",
        "assignment_group": "Analytics Settings Managers",
        "description": "This is new tool code implementation testing for Database_Incident",
        "caller_username": "survey.user",
        "incident_number": "312321223",
        "http_code": 201,
    }

    # Patch `get_servicenow_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.servicenow.create_an_incident.get_servicenow_client"
    ) as mock_servicenow_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_servicenow_client.return_value = mock_client
        mock_client.post_request.return_value = {
            "result": {
                "number": test_data["incident_number"],
                "short_description": test_data["short_description"],
            },
            "status_code": test_data["http_code"],
        }

        # Create an incident
        response = create_an_incident(
            short_description=test_data["short_description"],
            impact_value=test_data["impact_value"],
            urgency_value=test_data["urgency_value"],
            incident_category=test_data["incident_category"],
            assignment_group=test_data["assignment_group"],
            description=test_data["description"],
            caller_username=test_data["caller_username"],
        )

        # Ensure that create_an_incident() executed and returned proper values
        assert response
        assert response.http_code == test_data["http_code"]
        assert response.incident_number == test_data["incident_number"]
        assert response.short_description == test_data["short_description"]

        # Ensure the API call was made with expected parameters
        mock_client.post_request.assert_called_once_with(
            entity="incident",
            payload={
                "short_description": test_data["short_description"],
                "impact": test_data["impact_value"],
                "urgency": test_data["urgency_value"],
                "category": test_data["incident_category"],
                "assignment_group": test_data["assignment_group"],
                "description": test_data["description"],
                "caller_id": test_data["caller_username"],
            },
        )
