from unittest.mock import MagicMock, patch

from agent_ready_tools.clients.dnb_client import DNBClient


@patch("requests.post")
def test_dnb_client(mock_post: MagicMock) -> None:
    """
    Test that the `DNBClient` is working as expected.

    Args:
        mock_post: The mock for the requests.post function
    """

    # Define mock API response data
    test_data = {"access_token": "NmUzYWM4MWYxMDAwMTZl"}

    # Create a mock instance for API requests
    mock_client = MagicMock()
    mock_client.json.return_value = test_data
    mock_post.return_value = mock_client  # Set the mock return value

    # Call the DnB client
    response: DNBClient = DNBClient("", "", "", "")

    # Ensure that DNBClient() executed and returned proper values
    assert response
    assert response.bearer_token == test_data["access_token"]

    # Ensure the API call was made with expected parameters
    mock_client.json.assert_called_once()
