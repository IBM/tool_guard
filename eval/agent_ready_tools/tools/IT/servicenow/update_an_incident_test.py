from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.servicenow.update_an_incident import update_an_incident


def test_update_an_incident() -> None:
    """Test that the incident can be updated successfully by the `update_an_incident` tool."""

    # Define test data:
    test_data = {
        "incident_number_system_id": "96ada45083d8aa10e73115a6feaad37c",
        "short_description": "ATF through Agent11",
        "description": "Agent tool",
        "category_system_id": "Software",
        "impact_value": "3",
        "urgency_value": "3",
        "primary_contact": "John21 Doe",
        "comments": "This is to test comments",
        "work_notes": "This is to test work notes",
        "http_code": 200,
    }

    # Patch `get_servicenow_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.servicenow.update_an_incident.get_servicenow_client"
    ) as mock_servicenow_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_servicenow_client.return_value = mock_client
        mock_client.patch_request.return_value = {"status_code": test_data["http_code"]}

        # Update an incident
        response = update_an_incident(
            incident_number_system_id=test_data["incident_number_system_id"],
            short_description=test_data["short_description"],
            description=test_data["description"],
            category_system_id=test_data["category_system_id"],
            impact_value=test_data["impact_value"],
            urgency_value=test_data["urgency_value"],
            comments=test_data["comments"],
            work_notes=test_data["work_notes"],
        )

        # Ensure that update_an_incident() executed and returned proper values
        assert response
        assert response.http_code == 200

        # Ensure the API call was made with expected parameters
        mock_client.patch_request.assert_called_once_with(
            entity="incident",
            entity_id=test_data["incident_number_system_id"],
            payload={
                "short_description": test_data["short_description"],
                "description": test_data["description"],
                "category": test_data["category_system_id"],
                "impact": test_data["impact_value"],
                "urgency": test_data["urgency_value"],
                "comments": test_data["comments"],
                "work_notes": test_data["work_notes"],
            },
        )
