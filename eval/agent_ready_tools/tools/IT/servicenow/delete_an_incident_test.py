from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.servicenow.delete_an_incident import delete_an_incident


def test_delete_an_incident() -> None:
    """Test that an incident can be deleted successfully by the `delete_an_incident` tool."""
    # Define test data:
    test_data = {"id": "1100", "http_code": 201}

    # Patch `get_servicenow_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.servicenow.delete_an_incident.get_servicenow_client"
    ) as mock_servicenow_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_servicenow_client.return_value = mock_client
        mock_client.delete_request.return_value = test_data["http_code"]

        # Delete an incident
        response = delete_an_incident(incident_number_system_id=test_data["id"])

        # Ensure that delete_an_incident() executed and returned proper values
        assert response
        assert response.http_code == test_data["http_code"]

        # Ensure the API call was made with expected parameters
        mock_client.delete_request.assert_called_once_with(
            entity="incident", entity_id=test_data["id"]
        )
