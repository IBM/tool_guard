from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.servicenow.get_states import get_states


def test_get_states() -> None:
    """Test that retrieves all the states successfully by the `get_states` tool."""

    # Define test data:
    test_data = {
        "label": "Closed Complete",
        "value": "3",
    }

    # Patch `get_servicenow_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.servicenow.get_states.get_servicenow_client"
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

        # Get states
        response = get_states()

        # Ensure that get_states() executed and returned proper values
        assert response
        assert len(response.states_list)
        assert response.states_list[0].state_code == test_data["value"]
        assert response.states_list[0].state_name == test_data["label"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            entity="sys_choice", params={"name": "task", "element": "state"}
        )
