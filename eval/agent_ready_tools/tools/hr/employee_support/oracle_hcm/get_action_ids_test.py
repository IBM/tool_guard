from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.oracle_hcm.get_action_ids import get_action_ids


def test_get_action_ids() -> None:
    """Tests that the `get_action_ids` function returns the expected response."""

    # Define test data:
    test_data = {
        "action_name": "Add Assignment",
        "action_id": 300000000118910,
    }

    # Patch `get_oracle_hcm_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.oracle_hcm.get_action_ids.get_oracle_hcm_client"
    ) as mock_get_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "items": [
                {
                    "ActionName": test_data["action_name"],
                    "ActionId": test_data["action_id"],
                }
            ]
        }

        # Get actions ids
        response = get_action_ids()

        # Ensure that get_action_ids() returned proper list of address types
        assert response
        assert response.action_details_list
        assert response.action_details_list[0].action_name == test_data["action_name"]
        assert response.action_details_list[0].action_id == test_data["action_id"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            "actionsLOV",
        )
