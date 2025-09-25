from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.zendesk.add_tags import add_tags


def test_add_tags() -> None:
    """Verifies that the add_tags tool can successfully add the tags."""

    # Define test data
    test_data = {
        "module": "users",
        "module_record_id": "5633253550745",
        "tags": "Am",
    }

    # Patch `get_zendesk_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.zendesk.add_tags.get_zendesk_client"
    ) as mock_zendesk_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_zendesk_client.return_value = mock_client
        mock_client.put_request.return_value = {
            "tags": [test_data["tags"]],
        }

        # Add tags using the add_tags tool
        response = add_tags(
            module=test_data["module"],
            module_record_id=test_data["module_record_id"],
            tags=test_data["tags"],
        )

        # Ensure that add_tags() executed and returned the proper values
        assert response
        assert response.tags == [test_data["tags"]]

        # Ensure the API call was made with the expected parameters
        mock_client.put_request.assert_called_once_with(
            entity=f"{test_data['module']}/{test_data['module_record_id']}/tags",
            payload={
                "tags": [test_data["tags"]],
            },
        )
