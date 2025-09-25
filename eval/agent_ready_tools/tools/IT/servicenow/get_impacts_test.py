from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.servicenow.get_impacts import get_impacts


def test_get_impacts() -> None:
    """Test that the impact can be retrieved successfully by the `get_impacts` tool."""

    # Define test data:
    test_data = {
        "label": "Satisfied",
        "value": "b97e89b94a36231201676b73322a0311",
    }

    # Patch `get_servicenow_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.servicenow.get_impacts.get_servicenow_client"
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

        # Get impacts list
        response = get_impacts()

        # Ensure that get_impacts() executed and returned proper values
        assert response
        assert len(response.impacts)
        assert response.impacts[0].impact == test_data["label"]
        assert response.impacts[0].impact_value == test_data["value"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            entity="sys_choice", params={"name": "task", "element": "impact"}
        )
