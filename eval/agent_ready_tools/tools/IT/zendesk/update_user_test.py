from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.zendesk.update_user import zendesk_update_user


def test_zendesk_update_user() -> None:
    """Verifies that the `zendesk_update_user` tool can successfully update a Zendesk user."""

    # Define test data:
    test_data = {
        "user_id": "48417118028697",
        "notes": "update details",
    }

    # Patch `get_zendesk_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.zendesk.update_user.get_zendesk_client"
    ) as mock_zendesk_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_zendesk_client.return_value = mock_client

        # Mock the API response to match expected structure
        mock_client.patch_request.return_value = {"user": {"id": test_data["user_id"]}}

        # Update user
        response = zendesk_update_user(user_id=test_data["user_id"], notes=test_data["notes"])

        # Ensure that zendesk_update_user() executed and returned proper values
        assert response
        assert response.user_id == test_data["user_id"]

        # Ensure the API call was made with expected parameters
        mock_client.patch_request.assert_called_once_with(
            entity=f"users/{test_data['user_id']}",
            payload={
                "user": {
                    "notes": test_data["notes"],
                }
            },
        )
