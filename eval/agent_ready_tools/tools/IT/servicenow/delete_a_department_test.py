from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.servicenow.delete_a_department import delete_a_department


def test_delete_a_department() -> None:
    """Test that a department can be deleted successfully by the `delete_a_department` tool."""
    # Define test data:
    test_data = {"id": "1100", "http_code": 201}

    # Patch `get_servicenow_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.servicenow.delete_a_department.get_servicenow_client"
    ) as mock_servicenow_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_servicenow_client.return_value = mock_client
        mock_client.delete_request.return_value = test_data["http_code"]

        # Delete a department
        response = delete_a_department(department_name_system_id=test_data["id"])

        # Ensure that delete_a_department() executed and returned proper values
        assert response
        assert response.http_code == test_data["http_code"]

        # Ensure the API call was made with expected parameters
        mock_client.delete_request.assert_called_once_with(
            entity="cmn_department", entity_id=test_data["id"]
        )
