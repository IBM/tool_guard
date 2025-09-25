from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.zendesk.update_group import update_group


def test_update_group() -> None:
    """Verifies that the `update_group` tool can successfully update a group in Zendesk."""

    # Define test data
    test_data = {
        "group_id": "6346890810393",
        "new_group_name": "Support Team",
        "new_group_description": "Handles customer support inquiries",
        "updated_at": "2022-05-05T12:43:09Z",
    }

    # Patch `get_zendesk_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.zendesk.update_group.get_zendesk_client"
    ) as mock_zendesk_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_zendesk_client.return_value = mock_client
        mock_client.put_request.return_value = {
            "group": {
                "name": test_data["new_group_name"],
                "description": test_data["new_group_description"],
                "updated_at": test_data["updated_at"],
            }
        }

        # Update the group
        response = update_group(
            group_id=test_data["group_id"],
            new_group_name=test_data["new_group_name"],
            new_group_description=test_data["new_group_description"],
        )

        # Ensure that update_group() executed and returned proper values
        assert response
        assert response.name == test_data["new_group_name"]
        assert response.description == test_data["new_group_description"]
        assert response.updated_at == test_data["updated_at"]

        # Ensure the API call was made with expected parameters
        mock_client.put_request.assert_called_once_with(
            entity=f"groups/{test_data['group_id']}",
            payload={
                "group": {
                    "name": test_data["new_group_name"],
                    "description": test_data["new_group_description"],
                }
            },
        )
