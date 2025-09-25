from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.zendesk.delete_group import delete_group


def test_delete_group() -> None:
    """Tests that a group can be deleted successfully by the `delete_group` tool."""
    # Define test data:
    test_data = {"group_id": "48524098258841", "http_code": 204}

    # Patch `get_zendesk_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.zendesk.delete_group.get_zendesk_client"
    ) as mock_zendesk_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_zendesk_client.return_value = mock_client
        mock_client.delete_request.return_value = {"status_code": test_data["http_code"]}

        # Call the function
        response = delete_group(group_id=test_data["group_id"])

        # Ensure that the delete_group() has been executed and returned the expected response
        assert response
        assert response.http_code == test_data["http_code"]

        # Ensure the API call was made with expected parameters
        mock_client.delete_request.assert_called_once_with(entity=f"groups/{test_data['group_id']}")
