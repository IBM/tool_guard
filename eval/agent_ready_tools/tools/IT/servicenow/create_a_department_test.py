from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.servicenow.create_a_department import create_a_department


def test_create_a_department() -> None:
    """Test that department can be created successfully by the `create_a_department` tool."""

    # Define test data:
    test_data = {
        "department_name": "Global operations dept",
        "description": "Global operations manages the organization",
        "department_id": "1103",
    }

    # Patch `get_servicenow_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.servicenow.create_a_department.get_servicenow_client"
    ) as mock_servicenow_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_servicenow_client.return_value = mock_client
        mock_client.post_request.return_value = {"result": {"name": test_data["department_name"]}}

        # Create a department
        response = create_a_department(
            department_name=test_data["department_name"],
            description=test_data["description"],
            department_id=test_data["department_id"],
        )

        # Ensure that create_a_department() executed and returned proper values
        assert response
        assert response.department_name == test_data["department_name"]

        # Ensure the API call was made with expected parameters
        mock_client.post_request.assert_called_once_with(
            entity="cmn_department",
            payload={
                "name": test_data["department_name"],
                "description": test_data["description"],
                "id": test_data["department_id"],
            },
        )
