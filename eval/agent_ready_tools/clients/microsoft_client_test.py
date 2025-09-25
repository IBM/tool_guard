from unittest.mock import MagicMock, patch

from agent_ready_tools.clients.microsoft_client import MicrosoftClient


@patch("agent_ready_tools.clients.microsoft_client.msal.ConfidentialClientApplication")
def test_microsoft_client(mock_msal_client_app: MagicMock) -> None:
    """
    Test that the `MicrosoftClient` is working as expected.

    Args:
        mock_msal_client_app: The mock for the msal.ConfidentialClientApplication function
    """

    # Define mock API response data
    test_data = {"access_token": "NmUzYWM4MWYxMDAwMTZl"}

    # Create a mock instance for API requests
    mock_client = MagicMock()
    mock_msal_client_app.return_value = mock_client  # Set created mock for the MSAL object
    mock_client.get_accounts.return_value = ["mock_account"]
    mock_client.acquire_token_silent.return_value = None
    mock_client.acquire_token_for_client.return_value = test_data
    mock_client.acquire_token_by_username_password.return_value = test_data

    # Call the MicrosoftClient client
    response: MicrosoftClient = MicrosoftClient("", "", "", "", "", "")

    # Ensure that MicrosoftClient() executed and returned proper values
    assert response
    assert response.token == test_data["access_token"]

    # Ensure the API call was made with expected parameters
    mock_client.acquire_token_for_client.assert_called_once()
