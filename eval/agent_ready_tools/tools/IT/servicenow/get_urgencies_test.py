from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.servicenow.get_urgencies import get_urgencies


def test_get_urgencies() -> None:
    """Test that the urgency can be retrieved by the `get_urgencies` tool."""

    # Define test data:
    test_data = {
        "label": "Extreme",
        "value": "5",
    }

    # Patch `get_servicenow_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.servicenow.get_urgencies.get_servicenow_client"
    ) as mock_servicenow_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_servicenow_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "result": [
                {
                    "value": test_data["value"],
                    "label": test_data["label"],
                },
            ],
        }

        # Get assignment groups
        response = get_urgencies()

        # Ensure that get_assignment_groups() executed and returned proper values
        assert response
        assert len(response.urgencies)
        assert response.urgencies[0].urgency == test_data["label"]
        assert response.urgencies[0].urgency_value == test_data["value"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            entity="sys_choice", params={"name": "task", "element": "urgency"}
        )
