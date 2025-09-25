from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.zendesk.list_tags import list_tags


def test_list_tags() -> None:
    """Verifies that the list_tags tool can successfully retrieve the tags."""

    # Define test data
    test_data = {"module": "organizations", "module_record_id": "6288314909081", "tags": "captain"}

    # Patch `get_zendesk_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.zendesk.list_tags.get_zendesk_client"
    ) as mock_zendesk_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_zendesk_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "tags": [test_data["tags"]],
        }

        # Retrieve tags using the list_tags tool
        response = list_tags(
            module=test_data["module"],
            module_record_id=test_data["module_record_id"],
        )

        # Ensure that list_tags() executed and returned the proper values
        assert response
        assert response.tags == [test_data["tags"]]

        # Ensure the API call was made with the expected parameters
        mock_client.get_request.assert_called_once_with(
            entity=f"{test_data['module']}/{test_data['module_record_id']}/tags"
        )
