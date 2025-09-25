from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.servicenow.get_cost_centers import get_cost_centers


def test_get_cost_centers() -> None:
    """Test that cost centers can be retrieved successfully."""

    # Define test data:
    test_data = {
        "name": "Sales",
        "id": "7fb1cc99c0a80a6d30c04574d14c0acf",
    }

    # Patch `get_servicenow_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.servicenow.get_cost_centers.get_servicenow_client"
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

        # Get costs centers
        response = get_cost_centers(cost_center_name=test_data["name"])

        # Ensure that get_cost_centers() executed and returned proper values
        assert response
        assert len(response.cost_centers)
        assert response.cost_centers[0].system_id == test_data["id"]
        assert response.cost_centers[0].cost_center_name == test_data["name"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            entity="cmn_cost_center", params={"name": test_data["name"]}
        )
