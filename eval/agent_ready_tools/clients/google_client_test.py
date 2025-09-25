from unittest.mock import MagicMock, patch

from agent_ready_tools.clients.google_client import GoogleClient


def test_google_client() -> None:
    """Test that the `GoogleClient` is working as expected."""

    # Define mock API response data
    access_token = "NmUzYWM4MWYxMDAwMTZl"

    # Patch GoogleAuthManager to mock its behavior
    with patch("agent_ready_tools.clients.google_client.GoogleAuthManager") as mock_auth_manager:
        # Create a mock for the GoogleClient's instance
        mock_client = MagicMock()
        mock_client.get_bearer_token.return_value = access_token
        mock_auth_manager.return_value = mock_client

        # Create the GoogleClient instance
        client: GoogleClient = GoogleClient("", "", "", "", "", "")

        # Call get_bearer_token function from GoogleClient client
        response = client.auth_manager.get_bearer_token()

        # Ensure that get_bearer_token() executed and returned proper values
        assert response == access_token

        # Ensure the GoogleClient API call was made with expected parameters
        mock_client.get_bearer_token.assert_called_once_with()
