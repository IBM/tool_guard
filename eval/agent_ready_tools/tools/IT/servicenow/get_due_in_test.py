from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.servicenow.get_due_in import get_due_in


def test_get_due_in() -> None:
    """Test that all the due-in can be retrieved successfully."""

    # Define test data:
    test_data = {
        "due": "1 Hour",
    }

    # Patch `get_servicenow_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.servicenow.get_due_in.get_servicenow_client"
    ) as mock_servicenow_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_servicenow_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "result": [
                {
                    "label": test_data["due"],
                    "value": test_data["due"],
                },
            ],
        }

        # Get due-in records
        response = get_due_in()

        # Ensure that get_due_in() executed and returned proper values
        assert response
        assert len(response.due_in_list)
        assert response.due_in_list[0].due_in == test_data["due"]
        assert response.due_in_list[0].due_in_value == test_data["due"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            entity="sys_choice", params={"name": "alm_asset", "element": "due_in"}
        )
