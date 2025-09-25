from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.servicenow.get_workflow_states import get_workflow_states


def test_get_workflow_state() -> None:
    """Test that the `get_workflow_state` function returns the expected response."""

    # Define test data:
    test_data = {
        "label": "Finished",
        "value": "5",
    }

    # Patch `get_servicenow_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.servicenow.get_workflow_states.get_servicenow_client"
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

        # Get workflow states
        response = get_workflow_states()

        # Ensure that get_workflow_states() executed and returned proper values
        assert response
        assert len(response.workflow_state)
        assert response.workflow_state[0].work_flow_state_value == test_data["value"]
        assert response.workflow_state[0].work_flow_state == test_data["label"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            entity="sys_choice", params={"name": "kb_knowledge", "element": "workflow_state"}
        )
