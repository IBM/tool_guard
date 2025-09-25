from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.servicenow.get_priorities import get_priorities


def test_get_priorities() -> None:
    """Test that the `get_priorities` function returns the expected response."""

    # Define test data:
    test_data = {
        "priority": "5 - Planning",
        "priority_value": "5",
    }

    # Patch `get_servicenow_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.servicenow.get_priorities.get_servicenow_client"
    ) as mock_servicenow_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_servicenow_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "result": [
                {
                    "label": test_data["priority"],
                    "value": test_data["priority_value"],
                },
            ],
        }

        # Get priorities
        response = get_priorities()

        # Ensure that get_priorities() executed and returned proper values
        assert response
        assert len(response.system_choice)
        assert response.system_choice[0].priority == test_data["priority"]
        assert response.system_choice[0].priority_value == test_data["priority_value"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            entity="sys_choice", params={"name": "task", "element": "priority"}
        )
