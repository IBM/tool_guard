from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.servicenow.get_install_status import get_install_status


def test_get_install_status() -> None:
    """Test that all install statuses can be retrieved successfully."""

    # Define test data:
    test_data = {
        "label": "In use",
        "id": "04d7f748e492021008dda4ccc400805a",
    }

    # Patch `get_servicenow_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.servicenow.get_install_status.get_servicenow_client"
    ) as mock_servicenow_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_servicenow_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "result": [
                {
                    "sys_id": test_data["id"],
                    "label": test_data["label"],
                },
            ],
        }

        # Get installation status
        response = get_install_status()

        # Ensure that get_install_status() executed and returned proper values
        assert response
        assert len(response.install_status_list)
        assert response.install_status_list[0].system_id == test_data["id"]
        assert response.install_status_list[0].install_status == test_data["label"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            entity="sys_choice", params={"name": "alm_asset", "element": "install_status"}
        )
