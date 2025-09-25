from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.servicenow.get_assignment_groups import get_assignment_groups


def test_get_assignment_groups() -> None:
    """Test that all the assignment groups can be retrieved successfully."""

    # Define test data:
    test_data = {
        "name": "eCAB Approval",
        "id": "b97e89b94a36231201676b73322a0311",
    }

    # Patch `get_servicenow_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.servicenow.get_assignment_groups.get_servicenow_client"
    ) as mock_servicenow_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_servicenow_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "result": [
                {
                    "sys_id": test_data["id"],
                    "name": test_data["name"],
                },
            ],
        }

        # Get assignment groups
        response = get_assignment_groups(
            assignment_group=test_data["name"], system_id=test_data["id"]
        )

        # Ensure that get_assignment_groups() executed and returned proper values
        assert response
        assert len(response.assignment_groups)
        assert response.assignment_groups[0].system_id == test_data["id"]
        assert response.assignment_groups[0].assignment_group == test_data["name"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            entity="sys_user_group", params={"name": test_data["name"], "sys_id": test_data["id"]}
        )
