from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.zendesk.update_user_identity import update_user_identity


def test_update_user_identity() -> None:
    """Verifies that the `update_user_identity` tool can successfully update a Zendesk user."""

    # Define test data:
    test_data = {
        "user_id": "48524577328409",
        "user_identity_id": "48524658495769",
        "value": "jaggu@gmail.com",
    }

    # Patch `get_zendesk_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.zendesk.update_user_identity.get_zendesk_client"
    ) as mock_zendesk_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_zendesk_client.return_value = mock_client

        # Mock the API response to match expected structure
        mock_client.patch_request.return_value = {"identity": {"id": test_data["user_identity_id"]}}

        # Update user identity
        response = update_user_identity(
            user_id=test_data["user_id"],
            user_identity_id=test_data["user_identity_id"],
            value=test_data["value"],
        )

        # Ensure that update_user_identity() executed and returned proper values
        assert response
        assert response.user_identity_id == test_data["user_identity_id"]

        # Ensure the API call was made with expected parameters
        mock_client.patch_request.assert_called_once_with(
            entity=f"users/{test_data['user_id']}/identities/{test_data['user_identity_id']}",
            payload={
                "identity": {
                    "value": test_data["value"],
                    "primary": False,
                }
            },
        )
