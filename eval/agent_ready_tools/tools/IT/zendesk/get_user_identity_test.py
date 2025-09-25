from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.zendesk.get_user_identity import get_user_identity


def test_get_user_identity() -> None:
    """Test that `get_user_identity` returns all the identities of the user."""

    # Sample user ID and mock identity data
    test_data = {
        "user_id": "48524577328409",
        "identity_id": "48524658495769",
        "identity_type": "email",
        "value": "jaggu@gmail.com",
        "primary": False,
    }

    # Patch `get_zendesk_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.zendesk.get_user_identity.get_zendesk_client"
    ) as mock_zendesk_client:
        mock_client = MagicMock()
        mock_zendesk_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "identities": [
                {
                    "id": test_data["identity_id"],
                    "type": test_data["identity_type"],
                    "value": test_data["value"],
                    "primary": test_data["primary"],
                }
            ]
        }

        # Call the function
        response = get_user_identity(user_id=test_data["user_id"], identity_type="email")

        assert response
        assert response.identities[0].identity_id == test_data["identity_id"]
        assert response.identities[0].identity_type == test_data["identity_type"]
        assert response.identities[0].value == test_data["value"]
        assert response.identities[0].primary == test_data["primary"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            entity=f"users/{test_data["user_id"]}/identities", params={"type[]": "email"}
        )
