from unittest.mock import MagicMock, patch

from agent_ready_tools.clients.sterling_oms_client import SterlingOMSClient


@patch("requests.get")
@patch("requests.post")
def test_watson_commerce_client(mock_post: MagicMock, mock_get: MagicMock) -> None:
    """
    Test that the Sterling OMS is working as expected.

    Args:
        mock_post: The mock for the requests.post function
        mock_get: The mock for the requests.get function
    """

    # Define mock API response data
    test_data_post = {"UserToken": "F6cBukdEEJYpKG2YjYmfavxxa7l81u2h"}

    # Create a mock instance for API requests
    mock_response_post = MagicMock()
    mock_response_post.json.return_value = test_data_post
    mock_post.return_value = mock_response_post

    test_status_code_get = 200
    test_text_get = "eyJraWQiOiJkZW1vMi1ub25wcm9kIiwiYWxnIjoiUlMyN"

    mock_response_get = MagicMock()
    mock_response_get.status_code = test_status_code_get
    mock_response_get.text = test_text_get
    mock_get.return_value = mock_response_get

    # Call the client
    client: SterlingOMSClient = SterlingOMSClient("", "", "", "", "")

    # Ensure that WatsonCommerceClient() executed and returned proper values
    assert client
    assert client.user_token == test_data_post["UserToken"]
    assert client.jwt_token == test_text_get

    # Ensure the API call was made with expected parameters
    mock_get.assert_called_once()
    mock_post.assert_called_once()
