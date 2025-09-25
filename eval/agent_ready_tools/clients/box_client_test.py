import time
from unittest.mock import MagicMock, patch

from agent_ready_tools.clients.box_client import BoxClient


@patch("requests.post")
def test_box_client(mock_post: MagicMock) -> None:
    """
    Test that the `BoxClient` is working as expected.

    Args:
        mock_post: The mock for the requests.post function
    """

    # Define mock API response data
    test_data = {"access_token": "NmUzYWM4MWYxMDAwMTZl", "expires_in": 3600}

    # Create a mock instance for API requests
    mock_client = MagicMock()
    mock_client.json.return_value = test_data  # Simulate JSON response
    mock_client.raise_for_status = MagicMock()  # Simulate successful request
    mock_post.return_value = mock_client  # Set created mock for the post function

    # Call the BOX client
    response: BoxClient = BoxClient("", "", "", "", "", "")

    # Ensure that BoxClient() executed and returned proper values
    assert response
    assert response.auth["token"] == test_data["access_token"]
    assert response.auth["expires"] > time.time()

    # Ensure the API call was made with expected parameters
    mock_client.json.assert_called_once()
